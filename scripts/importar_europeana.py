#!/usr/bin/env python3
"""
Busca fotos históricas de Vigo en Europeana y las guarda en un fichero aparte
para revisarlas antes de publicarlas. No modifica data/fotos.json.

    python3 scripts/importar_europeana.py --salida importacion/resultado.json

Criterios:
  * Solo licencias libres: dominio público (PDM), CC0, CC BY y CC BY-SA.
  * Solo imágenes con dirección directa a la imagen (edmIsShownBy).
  * Solo Vigo (Galicia): se descartan homónimos como Vigo di Fassa o Vigo
    Rendena (Italia) y apellidos.
  * Hasta el año límite (1982 por defecto).
  * Se omiten las que ya están en data/fotos.json o en data/excluidas.json.

Usa la clave pública de demostración de Europeana ("api2demo") salvo que se
indique otra con la variable de entorno EUROPEANA_KEY.
"""
import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FOTOS = RAIZ / "data" / "fotos.json"
EXCLUIDAS = RAIZ / "data" / "excluidas.json"
API = "https://api.europeana.eu/record/v2/search.json"
UA = "VigoVello/0.3 (https://github.com/asergom/vigovello)"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importar_commons import Ubicador, LUGARES, NOTA_SIN_UBICAR  # noqa: E402

LICENCIAS = [
    (r"publicdomain/mark", "PDM"),
    (r"publicdomain/zero", "CC0"),
    (r"licenses/by-sa/", "CC BY-SA"),
    (r"licenses/by/", "CC BY"),
]
NO_VIGO = ["fassa", "rendena", "trentino", "trento", "vigo di", "vigò", "vigo im", "vigo cavedine",
           "vigolo", "méndez vigo", "mendez vigo", "manuel vigo"]
SI_GALICIA = ["galicia", "galiza", "pontevedra", "españa", "espana", "spain", "spanje", "spanien", "espagne",
              "ria de vigo", "ría de vigo", "bahia de vigo", "bahía de vigo", "vigo bay"]


def normalizar(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def pedir(params):
    url = API + "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for intento in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            espera = 2 ** intento
            print(f"  aviso: {e!r}; reintento en {espera}s", flush=True)
            time.sleep(espera)
    raise RuntimeError("Europeana no responde")


def primero(v):
    if isinstance(v, list):
        return v[0] if v else ""
    if isinstance(v, dict):
        for k in ("es", "gl", "def", "en"):
            if v.get(k):
                return primero(v[k])
        return primero(next(iter(v.values()), ""))
    return v or ""


def licencia(item):
    r = primero(item.get("rights"))
    for patron, nombre in LICENCIAS:
        if re.search(patron, r):
            if nombre in ("CC BY-SA", "CC BY"):
                m = re.search(r"/(\d\.\d)", r)
                nombre += f" {m.group(1)}" if m else ""
            return nombre, r
    return None, r


def anio(item):
    for campo in ("year",):
        for v in item.get(campo) or []:
            m = re.search(r"(1[89]\d\d|20[0-2]\d)", str(v))
            if m:
                return int(m.group(1)), False
    texto = " ".join(str(x) for x in (item.get("edmTimespanLabel") or []))
    texto += " " + " ".join(str(x) for x in (item.get("dcDate") or []))
    anios = [int(a) for a in re.findall(r"(1[89]\d\d|20[0-2]\d)", texto)]
    if anios:
        return min(anios), True
    return None, False


def es_vigo(item, texto):
    t = normalizar(texto)
    if not re.search(r"\bvigo\b", t):
        return False
    if any(normalizar(x) in t for x in NO_VIGO):
        return False
    lat = item.get("edmPlaceLatitude") or []
    if any(abs(float(x) - 42.24) < 0.3 for x in lat if re.match(r"-?\d", str(x))):
        return True
    proveedor = normalizar(primero(item.get("dataProvider")) + " " + primero(item.get("provider")))
    if any(p in proveedor for p in ("galiciana", "hispana", "biblioteca nacional", "espana", "galicia")):
        return True
    return any(normalizar(x) in t for x in SI_GALICIA)


def https(url):
    return re.sub(r"^http://", "https://", url or "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", required=True)
    ap.add_argument("--hasta", type=int, default=1982)
    ap.add_argument("--maximo", type=int, default=3000, help="Número máximo de registros a revisar")
    args = ap.parse_args()

    clave = os.environ.get("EUROPEANA_KEY", "api2demo")
    ubicador = Ubicador(LUGARES)

    def cargar(r):
        if not r.exists():
            return []
        d = json.loads(r.read_text(encoding="utf-8"))
        return d.get("fotos", d) if isinstance(d, dict) else d
    conocidas = {f.get("url_fuente") for f in cargar(FOTOS)} | {e if isinstance(e, str) else e.get("url_fuente") for e in cargar(EXCLUIDAS)}

    consultas = ["Vigo", "Vigo AND (Galicia OR Pontevedra OR postal OR fotografía OR vista)"]
    nuevas, vistos, motivos = [], set(), {}

    def descartar(m):
        motivos[m] = motivos.get(m, 0) + 1

    for q in consultas:
        cursor, revisados = "*", 0
        print(f"· consulta: {q}", flush=True)
        while cursor and revisados < args.maximo:
            d = pedir({"wskey": clave, "query": q, "reusability": "open", "media": "true",
                       "qf": "TYPE:IMAGE", "rows": 100, "profile": "rich", "cursor": cursor})
            items = d.get("items") or []
            if not items:
                break
            for it in items:
                revisados += 1
                if it.get("id") in vistos:
                    continue
                vistos.add(it.get("id"))
                titulo = primero(it.get("dcTitleLangAware")) or primero(it.get("title"))
                desc = primero(it.get("dcDescriptionLangAware")) or primero(it.get("dcDescription"))
                texto = " ".join([titulo, desc, " ".join(map(str, it.get("edmPlaceLabel") or [])),
                                  primero(it.get("dataProvider"))])
                nombre_lic, url_lic = licencia(it)
                if not nombre_lic:
                    descartar("licencia no libre"); continue
                imagen = https(primero(it.get("edmIsShownBy")))
                if not imagen:
                    descartar("sin imagen directa"); continue
                if not es_vigo(it, texto):
                    descartar("no es Vigo (Galicia)"); continue
                a, aprox = anio(it)
                if a and a > args.hasta:
                    descartar(f"posterior a {args.hasta}"); continue
                pagina = https(primero(it.get("edmIsShownAt"))) or ("https://www.europeana.eu/item" + it["id"])
                if pagina in conocidas or imagen in conocidas:
                    descartar("ya incluida o excluida"); continue
                l = ubicador.situar(texto)
                creador = primero(it.get("dcCreatorLangAware")) or primero(it.get("dcCreator"))
                if creador.startswith("http"):
                    creador = ""
                if normalizar(creador) in ("anonymous", "anonimo", "anónimo"):
                    creador = ""
                nuevas.append({
                    "id": "europeana-" + re.sub(r"[^A-Za-z0-9]+", "-", it["id"]).strip("-")[-60:],
                    "titulo": titulo.strip(" .[]"),
                    "lugar": l["nombre"],
                    "anio": a,
                    "aproximada": aprox,
                    "descripcion": (desc[:500] + (" " + NOTA_SIN_UBICAR if l.get("ubicacion") == "sin_confirmar" else "")).strip(),
                    "lat": l["lat"], "lng": l["lng"], "ubicacion": l.get("ubicacion", "sin_confirmar"),
                    "imagen": imagen,
                    "miniatura": https(primero(it.get("edmPreview"))) or imagen,
                    "original": imagen,
                    "autor": creador,
                    "fuente": primero(it.get("dataProvider")) or "Europeana",
                    "url_fuente": pagina,
                    "europeana": "https://www.europeana.eu/item" + it["id"],
                    "licencia": {"PDM": "PDM"}.get(nombre_lic, nombre_lic),
                    "url_licencia": url_lic,
                    "importada": True,
                })
                conocidas.add(pagina)
            cursor = d.get("nextCursor")
            print(f"  revisados {revisados} de {d.get('totalResults')}; candidatas {len(nuevas)}", flush=True)
            time.sleep(0.3)

    print(f"\nCandidatas: {len(nuevas)}")
    for m, n in sorted(motivos.items(), key=lambda x: -x[1]):
        print(f"  descartadas por {m}: {n}")
    proveedores = {}
    for f in nuevas:
        proveedores[f["fuente"]] = proveedores.get(f["fuente"], 0) + 1
    for p, n in sorted(proveedores.items(), key=lambda x: -x[1]):
        print(f"  {p}: {n}")
    Path(args.salida).parent.mkdir(parents=True, exist_ok=True)
    Path(args.salida).write_text(json.dumps({"fotos": nuevas}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
