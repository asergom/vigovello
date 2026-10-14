# VigoVello

Mapa de fotografías históricas de Vigo, al estilo de [OldNYC](https://www.oldnyc.org): cada punto del mapa es un lugar y, al pulsarlo, aparecen las fotos que se tomaron allí.

Es una web estática (HTML, CSS y JavaScript, sin compilar nada), así que se publica gratis con **GitHub Pages**.

**VigoVello no almacena fotografías.** Es solo un visor: `data/fotos.json` guarda, para cada foto, la dirección de la imagen en la web donde está alojada (Wikimedia Commons, archivos, bibliotecas…), su página de origen, su ubicación y sus datos. El navegador carga cada imagen directamente desde su origen, y el visor enlaza siempre a esa página.

## Estructura

```
index.html                 la web pública
editor.html                herramienta para situar fotos en el mapa
css/estilo.css             estilos
js/config.js               ajustes (centro del mapa, enlace al repo…)
js/app.js                  lógica del mapa, panel y visor
data/fotos.json            las fotos que salen en el mapa
img/logo-vv.svg            logo (aquí no se guardan fotos)
scripts/importar_commons.py  importa fotos antiguas de Wikimedia Commons
scripts/fuentes.json       colecciones de Commons que se importan
scripts/lugares.json       lugares de Vigo para situar fotos sin coordenadas
data/excluidas.json        fotos retiradas que no deben volver a importarse
CANDIDATAS.md              fotos encontradas pendientes de revisar
```

## Publicar en GitHub Pages

1. Crea un repositorio en GitHub (`vigovello`) y sube todo el contenido de esta carpeta.
2. En el repositorio: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, rama `main`, carpeta `/ (root)`.
3. En un par de minutos la web estará en `https://asergom.github.io/vigovello/`.

## Probarla en tu ordenador

El navegador no deja leer `data/fotos.json` si abres `index.html` con doble clic, así que lánzala con un servidor local:

```bash
python3 -m http.server 8000
```

y abre <http://localhost:8000>.

## Añadir fotos

### Desde Wikimedia Commons

`scripts/importar_commons.py` importa fotos de las colecciones de [`scripts/fuentes.json`](scripts/fuentes.json). Se ejecuta a mano, solo cuando se decida:

1. **Licencias:** solo acepta dominio público, CC0, CC BY y CC BY-SA. Descarta las «no comercial» (NC), «sin derivadas» (ND) y las desconocidas.
2. **Fechas:** descarta las fotos posteriores a 1980.
3. **Documentos:** descarta prensa, esquelas, actas y planos.
4. **Ubicación:** sitúa cada foto con sus coordenadas, con un lugar reconocido de [`scripts/lugares.json`](scripts/lugares.json) o, si no, en un punto orientativo con la etiqueta «Ubicación sin confirmar».
5. **Fotos existentes:** no modifica las que ya están en el mapa.

Para retirar una foto y que no vuelva a importarse, bórrala de `data/fotos.json` y añade la dirección de su ficha a `data/excluidas.json`:

```json
{"fotos": ["https://commons.wikimedia.org/wiki/File:Nombre_del_archivo.jpg"]}
```

Para probarlo en tu ordenador sin escribir nada: `python3 scripts/importar_commons.py --simular`.

### Corregir ubicaciones con el editor

No es necesario para publicar: las fotos sin ubicación ya aparecen en el mapa con su etiqueta. El editor sirve para ir mejorándolas, por ejemplo al validar propuestas de los visitantes.

1. Abre `https://asergom.github.io/vigovello/editor.html` (o la versión local).
2. La lista muestra las fotos con la ubicación sin confirmar. Elige una, haz clic en el mapa donde se tomó y pulsa **Guardar y siguiente**.
3. Pulsa **Descargar fotos.json** y sustituye `data/fotos.json` en el repositorio.

Para que varias fotos se agrupen en el mismo punto (como en OldNYC), haz clic sobre un punto existente: el editor copia sus coordenadas exactas y el nombre del lugar.

### Fotos de otras webs

En el editor pulsa **+ Añadir foto por URL** y pega la dirección de la imagen tal como está alojada en su web (y, si existe, la de una versión pequeña para la miniatura), junto con la página de origen. Solo se admiten direcciones `https://`: nunca se copian imágenes al repositorio.

Algunas webs no permiten mostrar sus imágenes desde otros sitios. Si una imagen no carga, la web lo indica en su lugar y sigue ofreciendo el enlace a la página original. Antes de enlazar fotos de un archivo, comprueba sus condiciones de uso.

## Formato de cada foto

```json
{
  "id": "commons-123456",
  "titulo": "Soportales del Berbés",
  "lugar": "O Berbés",
  "anio": 1900,
  "aproximada": true,
  "fecha": "",
  "descripcion": "…",
  "lat": 42.2388,
  "lng": -8.7264,
  "ubicacion": "aproximada",
  "imagen": "https://…/1280px-….jpg",
  "miniatura": "https://…/500px-….jpg",
  "original": "https://…/….jpg",
  "autor": "…",
  "fuente": "Wikimedia Commons",
  "url_fuente": "https://commons.wikimedia.org/wiki/File:…",
  "licencia": "Public domain"
}
```

`original` es opcional: si la imagen reducida no carga, la web lo intenta con esta dirección.

`fecha` es opcional: si está, se muestra tal cual («verano de 1924», «1910–1915»); si no, se usa `anio`.

## Ubicaciones sin confirmar y propuestas de los visitantes

Cada foto tiene un campo `ubicacion`:

- `confirmada`: el lugar es seguro.
- `aproximada`: la zona es correcta, pero el punto exacto no.
- `sin_confirmar`: no se sabe dónde se tomó. Se sitúa de forma orientativa, el punto se dibuja hueco y la foto lleva la etiqueta «Ubicación sin confirmar».

En el visor, cualquier visitante puede pulsar **Proponer ubicación**, marcar un punto en el mapa y añadir un comentario. Se abre una propuesta (issue) en GitHub con las coordenadas, un enlace al mapa y a la foto. Hace falta una cuenta gratuita de GitHub.

Para validar una propuesta, revísala en la pestaña **Issues** del repositorio. Si es correcta, cambia `lat`, `lng` y `ubicacion` de esa foto en `data/fotos.json` (o con el editor) y cierra el issue.

## Enlaces directos

- `#lugar=42.23955,-8.72230` abre el panel de un lugar.
- `#foto=commons-123456` abre una foto concreta.

## Derechos de las imágenes

Usa solo fotos de dominio público, con licencia libre o con permiso expreso de sus titulares, y mantén siempre el crédito. Fondos como el Arquivo Pacheco o los de prensa tienen derechos: para incluirlos hay que pedir autorización.

## Créditos

Mapa base © colaboradores de OpenStreetMap. Mapa interactivo con [Leaflet](https://leafletjs.com). Idea original: [OldNYC](https://www.oldnyc.org), de Dan Vanderkam.

## Licencia

El código, el diseño y el logo de VigoVello se publican con licencia [MIT](LICENSE).

Las fotografías **no** están cubiertas por esa licencia: cada una conserva la suya (dominio público, Creative Commons…), que se indica junto a la imagen en la web y en `data/fotos.json`.
