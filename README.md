# VigoVello

Mapa de fotografías históricas de Vigo, al estilo de [OldNYC](https://www.oldnyc.org): cada punto del mapa es un lugar y, al pulsarlo, aparecen las fotos que se tomaron allí.

Es una web estática (HTML, CSS y JavaScript, sin compilar nada), así que se publica gratis con **GitHub Pages**.

## Estructura

```
index.html                 la web pública
editor.html                herramienta para situar fotos en el mapa
css/estilo.css             estilos
js/config.js               ajustes (centro del mapa, enlace al repo…)
js/app.js                  lógica del mapa, panel y visor
data/fotos.json            las fotos que salen en el mapa
data/pendientes.json       fotos importadas que aún no tienen ubicación
img/                       aquí van tus propias fotos, si las alojas en el repo
scripts/importar_commons.py  importa fotos antiguas de Wikimedia Commons
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

### Desde Wikimedia Commons (dominio público y licencias libres)

```bash
python3 scripts/importar_commons.py --quitar-ejemplos
```

- Las fotos **con coordenadas** se añaden directamente a `data/fotos.json`.
- Las fotos **sin coordenadas** (la mayoría de las antiguas) van a `data/pendientes.json`.

Opciones útiles: `--hasta 1975` (año máximo), `--profundidad 3` (niveles de subcategorías), `--categoria "Category:Port of Vigo"` (se puede repetir), `--incluir-sin-fecha`.

Las imágenes no se descargan: se enlazan desde Commons, que lo permite, y cada foto muestra su autor, fuente y licencia.

### Situar fotos a mano con el editor

1. Abre `http://localhost:8000/editor.html`.
2. Elige una foto de la lista, haz clic en el mapa donde se tomó y completa título, lugar y año.
3. Pulsa **Descargar fotos.json** y **Descargar pendientes.json**, y sustituye los de `data/`.
4. Haz commit y push.

Para que varias fotos se agrupen en el mismo punto (como en OldNYC), haz clic sobre un punto rojo existente: el editor copia sus coordenadas exactas y el nombre del lugar.

### Tus propias fotos

Copia la imagen a `img/` (mejor en JPG de unos 1.200–1.600 px de ancho), y en el editor pulsa **+ Añadir foto propia** y escribe `img/nombre-del-archivo.jpg`.

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
  "imagen": "https://…/1280px-….jpg",
  "miniatura": "https://…/400px-….jpg",
  "autor": "…",
  "fuente": "Wikimedia Commons",
  "url_fuente": "https://commons.wikimedia.org/wiki/File:…",
  "licencia": "Public domain"
}
```

`fecha` es opcional: si está, se muestra tal cual («verano de 1924», «1910–1915»); si no, se usa `anio`.

## Enlaces directos

- `#lugar=42.23955,-8.72230` abre el panel de un lugar.
- `#foto=commons-123456` abre una foto concreta.

## Derechos de las imágenes

Usa solo fotos de dominio público, con licencia libre o con permiso expreso de sus titulares, y mantén siempre el crédito. Fondos como el Arquivo Pacheco o los de prensa tienen derechos: para incluirlos hay que pedir autorización.

## Créditos

Mapa base © colaboradores de OpenStreetMap. Mapa interactivo con [Leaflet](https://leafletjs.com). Idea original: [OldNYC](https://www.oldnyc.org), de Dan Vanderkam.
