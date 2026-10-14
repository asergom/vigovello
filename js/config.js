// Ajustes generales de la web. Cambia aquí lo que necesites.
window.CONFIG = {
  // Centro y zoom inicial del mapa (Vigo centro)
  centro: [42.2360, -8.7230],
  zoom: 15,
  zoomMin: 12,
  zoomMax: 19,

  // Fichero con las fotos
  datos: 'data/fotos.json',

  // Enlace al repositorio de GitHub (para el botón "Colabora")
  repo: 'https://github.com/asergom/vigovello',

  // Teselas del mapa base. OpenStreetMap estándar; el gris se aplica por CSS.
  teselas: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  atribucion: '&copy; colaboradores de <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
};
