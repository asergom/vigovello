#!/usr/bin/env python3
"""
Importa fotos históricas de Vigo desde Wikimedia Commons a data/fotos.json.

Lo ejecuta automáticamente GitHub Actions (.github/workflows/importar.yml),
pero también se puede lanzar a mano:

    python3 scripts/importar_commons.py
    python3 scripts/importar_commons.py --simular      # no escribe nada

Qué hace:
  1. Recorre las categorías y búsquedas de scripts/fuentes.json.
  2. Solo acepta licencias libres: dominio público, CC0, CC BY y CC BY-SA
     (descarta NC, ND y cualquier licencia desconocida).
  3. Descarta fotos posteriores a 'hasta_anio' y, en colecciones no
     históricas, las que no tienen fecha.
  4. Sitúa cada foto: con sus coordenadas de Commons si las tiene; si no,
     buscando un lugar de scripts/lugares.json en su título, descripción y
     categorías; si no, en un punto por defecto marcado "sin_confirmar".
  5. Añade solo fotos nuevas: nunca toca las que ya están en fotos.json
     (así se conservan las correcciones manuales) ni las de data/excluidas.json.

Solo usa la librería estándar de Python.
"""

import argparse
import html
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
UA = "VigoVello/0.2 (https://github.com/asergom/vigovello)"

RAIZ = Path(__file__).resolve().parent.parent
FOTOS = RAIZ / "data" / "fotos.json"
EXCLUIDAS = RAIZ / "data" / "excluidas.json"
FUENTES = RAIZ / "scripts" / "fuentes.json"
LUGARES = RAIZ / "scripts" / "lugares.json"


# ---------------------------------------------------------------- API ----
def api(**params):
    params.update(format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for intento in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            espera = 2 ** intento
            print(f"  aviso: {e}; reintento en {espera}s", file=sys.stderr)
            time.sleep(espera)
    raise SystemExit("No se pudo contactar con Wikimedia Commons.")


def paginar(**params):
    cont = {}
    while True:
        datos = api(**params, **cont)
        yield datos
        if "continue" not in datos:
            break
        cont = datos["continue"]
        time.sleep(0.3)


PROPS = dict(prop="imageinfo|coordinates|categories", iiprop="url|extmetadata|mime|size",
             iiurlwidth="1280", colimit="max", cllimit="max", clshow="!hidden")


def subcategorias(cat, profundidad, vistas):
    if cat in vistas:
        return
    vistas.add(cat)
    yield cat
    if profundidad <= 0:
        return
    for datos in paginar(action="query", list="categorymembers", cmtitle=cat, cmtype="subcat", cmlimit="max"):
        for m in datos.get("query", {}).get("categorymembers", []):
            yield from subcategorias(m["title"], profundidad - 1, vistas)


def archivos_de_categoria(cat):
    for datos in paginar(action="query", generator="categorymembers", gcmtitle=cat,
                         gcmtype="file", gcmlimit="50", **PROPS):
        yield from datos.get("query", {}).get("pages", [])


def archivos_de_busqueda(texto):
    for datos in paginar(action="query", generator="search", gsrsearch=texto,
                         gsrnamespace="6", gsrlimit="50", **PROPS):
        yield from datos.get("query", {}).get("pages", [])


# --------------------------------------------------------- utilidades ----
def limpiar(texto):
    if not texto:
        return ""
    texto = re.sub(r"<[^>]+>", " ", str(texto))
    return re.sub(r"\s+", " ", html.unescape(texto)).strip()


def normalizar(texto):
    t = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def meta(m, campo):
    return limpiar((m.get(campo) or {}).get("value", ""))


def licencia_libre(m):
    """Devuelve el nombre de la licencia si es libre y aceptable, o None."""
    nombre = meta(m, "LicenseShortName")
    clave = normalizar(nombre + " " + meta(m, "License") + " " + meta(m, "UsageTerms"))
    if re.search(r"\b(nc|nd)\b|non-?commercial|no ?deriv|all rights reserved|fair use", clave):
        return None
    if re.search(r"public domain|dominio publico|\bpd\b|pd-|cc0|cc-zero|no restrictions|no known copyright", clave):
        return nombre or "Dominio público"
    if re.search(r"\bcc[ -]by(-sa)?\b|cc[ -]by[ -]sa|creative commons attribution", clave):
        return nombre or "Creative Commons"
    return None


def extraer_anio(m, texto_extra):
    for valor in (meta(m, "DateTimeOriginal"), meta(m, "DateTime"), texto_extra):
        anios = [int(a) for a in re.findall(r"\b(18[3-9]\d|19\d\d|20[0-2]\d)\b", valor)]
        if anios:
            aprox = bool(re.search(r"circa|\bca\.|\bc\.|hacia|aprox|\bh\.|entre|between|\d{4}s\b", valor, re.I))
            return min(anios), aprox, valor
    return None, False, ""


def titulo_archivo(p):
    return p["title"].removeprefix("File:")


def clave_archivo(url_o_titulo):
    """Clave común para reconocer el mismo archivo venga de donde venga."""
    t = urllib.parse.unquote(url_o_titulo.split("File:")[-1]).replace(" ", "_")
    return normalizar(t)


# ----------------------------------------------------------- lugares ----
class Ubicador:
    def __init__(self, ruta):
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        self.lugares = datos["lugares"]
        self.defecto = datos["por_defecto"]

    def situar(self, texto):
        t = normalizar(texto)
        for l in self.lugares:
            for c in l["claves"]:
                if re.search(r"\b" + re.escape(normalizar(c)) + r"\b", t):
                    return l
        return self.defecto


# ------------------------------------------------------------ convertir ----
def convertir(p, fuente, hasta, ubicador):
    info = (p.get("imageinfo") or [{}])[0]
    if not info.get("mime", "").startswith("image/") or info.get("mime") == "image/svg+xml":
        return None, "no es una imagen"
    m = info.get("extmetadata", {})

    licencia = licencia_libre(m)
    if not licencia:
        return None, "licencia no libre o desconocida"

    titulo_fich = titulo_archivo(p)
    nombre_limpio = re.sub(r"\.(jpe?g|png|tiff?|gif|webp)$", "", titulo_fich, flags=re.I).replace("_", " ")
    descripcion = meta(m, "ImageDescription")[:600]
    categorias = " ".join(c["title"].removeprefix("Category:") for c in p.get("categories", []))
    texto = " ".join([nombre_limpio, meta(m, "ObjectName"), descripcion, categorias])

    if fuente.get("solo_vigo") and "vigo" not in normalizar(texto):
        return None, "no es de Vigo"

    anio, aprox, fecha_txt = extraer_anio(m, nombre_limpio + " " + descripcion)
    if anio is None and not fuente.get("antiguas"):
        return None, "sin fecha en colección no histórica"
    if anio is not None and anio > hasta:
        return None, f"posterior a {hasta}"

    coords = (p.get("coordinates") or [None])[0]
    if coords:
        lat, lng, lugar, ubicacion = coords["lat"], coords["lon"], ubicador.situar(texto)["nombre"], "confirmada"
        if lugar == ubicador.defecto["nombre"]:
            lugar = ""
    else:
        l = ubicador.situar(texto)
        lat, lng, lugar, ubicacion = l["lat"], l["lng"], l["nombre"], l.get("ubicacion", "sin_confirmar")

    imagen = info.get("thumburl") or info.get("url")
    miniatura = re.sub(r"/(lossy-page1-)?\d+px-", lambda x: "/" + (x.group(1) or "") + "500px-", imagen) if "/thumb/" in imagen else imagen
    original = info.get("url") if not titulo_fich.lower().endswith((".tif", ".tiff")) else imagen

    if ubicacion == "sin_confirmar":
        nota = "No se ha podido ubicar: situada de forma orientativa."
        descripcion = (descripcion + " " + nota).strip() if descripcion else nota

    return {
        "id": f"commons-{p['pageid']}",
        "titulo": meta(m, "ObjectName") or nombre_limpio,
        "lugar": lugar,
        "anio": anio,
        "aproximada": aprox,
        "fecha": fecha_txt if fecha_txt and not re.fullmatch(r"\d{4}", fecha_txt) and len(fecha_txt) < 60 else "",
        "descripcion": descripcion,
        "lat": round(lat, 6),
        "lng": round(lng, 6),
        "ubicacion": ubicacion,
        "imagen": imagen,
        "miniatura": miniatura,
        "original": original,
        "autor": meta(m, "Artist")[:200],
        "fuente": "Wikimedia Commons",
        "url_fuente": info.get("descriptionurl", ""),
        "licencia": licencia,
        "importada": True,
    }, None


# ---------------------------------------------------------------- main ----
def cargar_lista(ruta):
    if not ruta.exists():
        return []
    d = json.loads(ruta.read_text(encoding="utf-8"))
    return d.get("fotos", d) if isinstance(d, dict) else d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--simular", action="store_true", help="Muestra qué haría sin escribir nada")
    args = ap.parse_args()

    fuentes = json.loads(FUENTES.read_text(encoding="utf-8"))
    hasta = fuentes.get("hasta_anio", 1980)
    ubicador = Ubicador(LUGARES)

    fotos = cargar_lista(FOTOS)
    excluidas = {clave_archivo(e if isinstance(e, str) else e.get("url_fuente", "")) for e in cargar_lista(EXCLUIDAS)}
    conocidas = {clave_archivo(f.get("url_fuente", "")) for f in fotos if f.get("url_fuente")} | excluidas
    conocidas |= {f["id"] for f in fotos}

    nuevas, motivos, vistas_pag = [], {}, set()

    def procesar(paginas, fuente):
        for p in paginas:
            if p.get("pageid") in vistas_pag or "imageinfo" not in p:
                continue
            vistas_pag.add(p.get("pageid"))
            k = clave_archivo(titulo_archivo(p))
            if k in conocidas or f"commons-{p.get('pageid')}" in conocidas:
                continue
            f, motivo = convertir(p, fuente, hasta, ubicador)
            if f:
                nuevas.append(f)
                conocidas.add(k)
            else:
                motivos[motivo] = motivos.get(motivo, 0) + 1

    vistas_cat = set()
    for fuente in fuentes.get("categorias", []):
        for cat in subcategorias(fuente["nombre"], fuente.get("profundidad", 1), vistas_cat):
            print("·", cat)
            procesar(archivos_de_categoria(cat), fuente)
    for fuente in fuentes.get("busquedas", []):
        print("· búsqueda:", fuente["texto"])
        procesar(archivos_de_busqueda(fuente["texto"]), fuente)

    sin_ub = sum(1 for f in nuevas if f["ubicacion"] == "sin_confirmar")
    print(f"\nRevisados {len(vistas_pag)} archivos en {len(vistas_cat)} categorías.")
    print(f"Nuevas: {len(nuevas)} ({sin_ub} sin ubicación confirmada).")
    for motivo, n in sorted(motivos.items(), key=lambda x: -x[1]):
        print(f"  descartadas por {motivo}: {n}")

    if args.simular or not nuevas:
        return
    FOTOS.write_text(json.dumps({"fotos": fotos + nuevas}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Guardado en {FOTOS.relative_to(RAIZ)}: {len(fotos) + len(nuevas)} fotos en total.")


if __name__ == "__main__":
    main()
