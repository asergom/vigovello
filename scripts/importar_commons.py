#!/usr/bin/env python3
"""
Importa fotos históricas de Vigo desde Wikimedia Commons.

Recorre una o varias categorías de Commons (y sus subcategorías), se queda con
las fotos anteriores al año límite y:

  * las que tienen coordenadas  -> se añaden a data/fotos.json
  * las que NO tienen coordenadas -> se guardan en data/pendientes.json
    para situarlas a mano con editor.html

Solo usa la librería estándar de Python. Ejemplos:

    python3 scripts/importar_commons.py
    python3 scripts/importar_commons.py --hasta 1975 --profundidad 3
    python3 scripts/importar_commons.py --categoria "Category:Port of Vigo"

Las fotos que ya estén en fotos.json (mismo id) no se duplican, así que puedes
ejecutarlo tantas veces como quieras.
"""

import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
# Wikimedia pide identificarse con un User-Agent descriptivo.
UA = "VigoVello/0.1 (https://github.com/asergom/vigovello)"

CATEGORIAS_POR_DEFECTO = [
    "Category:History of Vigo",
    "Category:Old photographs of Vigo",
    "Category:Black and white photographs of Vigo",
]

RAIZ = Path(__file__).resolve().parent.parent
FOTOS = RAIZ / "data" / "fotos.json"
PENDIENTES = RAIZ / "data" / "pendientes.json"


def api(**params):
    params.update(format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # red inestable o límite de peticiones
            espera = 2 ** intento
            print(f"  aviso: {e}; reintento en {espera}s", file=sys.stderr)
            time.sleep(espera)
    raise SystemExit("No se pudo contactar con Commons.")


def paginar(**params):
    """Recorre todas las páginas de resultados de la API."""
    cont = {}
    while True:
        datos = api(**params, **cont)
        yield datos
        if "continue" not in datos:
            break
        cont = datos["continue"]
        time.sleep(0.2)


def subcategorias(cat, profundidad, vistas):
    if cat in vistas:
        return
    vistas.add(cat)
    yield cat
    if profundidad <= 0:
        return
    for datos in paginar(action="query", list="categorymembers", cmtitle=cat,
                         cmtype="subcat", cmlimit="max"):
        for m in datos.get("query", {}).get("categorymembers", []):
            yield from subcategorias(m["title"], profundidad - 1, vistas)


def limpiar(texto):
    """Quita HTML de los metadatos de Commons."""
    if not texto:
        return ""
    texto = re.sub(r"<[^>]+>", " ", texto)
    return re.sub(r"\s+", " ", html.unescape(texto)).strip()


def extraer_anio(meta):
    for campo in ("DateTimeOriginal", "DateTime"):
        valor = limpiar(meta.get(campo, {}).get("value", ""))
        m = re.search(r"\b(18[4-9]\d|19\d\d|20[0-2]\d)\b", valor)
        if m:
            aprox = bool(re.search(r"circa|ca\.|c\.|hacia|aprox|\bh\.", valor, re.I))
            return int(m.group(1)), aprox, valor
    return None, False, ""


def fotos_de_categoria(cat):
    for datos in paginar(action="query", generator="categorymembers", gcmtitle=cat,
                         gcmtype="file", gcmlimit="50",
                         prop="imageinfo|coordinates",
                         iiprop="url|extmetadata|mime", iiurlwidth="1280",
                         colimit="max"):
        for p in datos.get("query", {}).get("pages", []):
            yield p


def convertir(p):
    info = (p.get("imageinfo") or [{}])[0]
    if not info.get("mime", "").startswith("image/"):
        return None
    meta = info.get("extmetadata", {})
    anio, aprox, fecha_txt = extraer_anio(meta)

    coords = (p.get("coordinates") or [None])[0]
    lat = coords.get("lat") if coords else None
    lng = coords.get("lon") if coords else None

    imagen = info.get("thumburl") or info.get("url")
    miniatura = re.sub(r"/\d+px-", "/400px-", imagen) if "/thumb/" in imagen else imagen

    titulo = p["title"].removeprefix("File:")
    titulo = re.sub(r"\.(jpe?g|png|tiff?|gif|webp)$", "", titulo, flags=re.I).replace("_", " ")

    return {
        "id": f"commons-{p['pageid']}",
        "titulo": limpiar(meta.get("ObjectName", {}).get("value")) or titulo,
        "lugar": "",
        "anio": anio,
        "aproximada": aprox,
        "fecha": fecha_txt if fecha_txt and not re.fullmatch(r"\d{4}", fecha_txt) else "",
        "descripcion": limpiar(meta.get("ImageDescription", {}).get("value"))[:600],
        "lat": round(lat, 6) if lat is not None else None,
        "lng": round(lng, 6) if lng is not None else None,
        "imagen": imagen,
        "miniatura": miniatura,
        "autor": limpiar(meta.get("Artist", {}).get("value"))[:200],
        "fuente": "Wikimedia Commons",
        "url_fuente": info.get("descriptionurl", ""),
        "licencia": limpiar(meta.get("LicenseShortName", {}).get("value")),
    }


def cargar(ruta):
    if ruta.exists():
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        return datos.get("fotos", datos) if isinstance(datos, dict) else datos
    return []


def guardar(ruta, fotos):
    ruta.write_text(json.dumps({"fotos": fotos}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--categoria", action="append", help="Categoría de Commons (se puede repetir)")
    ap.add_argument("--profundidad", type=int, default=2, help="Niveles de subcategorías (por defecto 2)")
    ap.add_argument("--hasta", type=int, default=1980, help="Año máximo de las fotos (por defecto 1980)")
    ap.add_argument("--incluir-sin-fecha", action="store_true", help="Incluir fotos sin fecha reconocible")
    ap.add_argument("--quitar-ejemplos", action="store_true", help="Borrar las fotos de ejemplo (id que empieza por 'ej-')")
    args = ap.parse_args()

    categorias = args.categoria or CATEGORIAS_POR_DEFECTO
    vistas = set()
    todas = []
    for raiz in categorias:
        for cat in subcategorias(raiz, args.profundidad, vistas):
            print(f"· {cat}")
            todas.extend(fotos_de_categoria(cat))

    nuevas, sin_coords, vistos = [], [], set()
    for p in todas:
        if p.get("pageid") in vistos:
            continue
        vistos.add(p.get("pageid"))
        f = convertir(p)
        if not f:
            continue
        if f["anio"] is None and not args.incluir_sin_fecha:
            continue
        if f["anio"] is not None and f["anio"] > args.hasta:
            continue
        (nuevas if f["lat"] is not None else sin_coords).append(f)

    fotos = cargar(FOTOS)
    if args.quitar_ejemplos:
        fotos = [f for f in fotos if not str(f.get("id", "")).startswith("ej-")]
    ids = {f.get("id") for f in fotos}
    añadidas = [f for f in nuevas if f["id"] not in ids]
    guardar(FOTOS, fotos + añadidas)

    pendientes = cargar(PENDIENTES)
    ids_p = {f.get("id") for f in pendientes} | ids
    pend_nuevas = [f for f in sin_coords if f["id"] not in ids_p]
    guardar(PENDIENTES, pendientes + pend_nuevas)

    print(f"\n{len(vistas)} categorías revisadas, {len(vistos)} archivos.")
    print(f"Añadidas al mapa: {len(añadidas)}  ->  {FOTOS.relative_to(RAIZ)}")
    print(f"Sin coordenadas (para situar a mano): {len(pend_nuevas)}  ->  {PENDIENTES.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
