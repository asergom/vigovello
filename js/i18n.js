// Idiomas de la web. Todo el texto visible sale de aquí o del campo "textos"
// de cada foto, para que nunca se mezclen idiomas.
(function () {
  'use strict';

  // Banderas simplificadas en SVG (las banderas son de dominio público).
  let nBandera = 0;
  const BANDERAS = {
    es: () => '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#AA151B"/><rect y="5" width="30" height="10" fill="#F1BF00"/></svg>',
    gl: () => '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#fff"/><polygon points="0,0 5,0 30,16.7 30,20 25,20 0,3.3" fill="#009AD8"/></svg>',
    en: () => {
      const id = 'uj' + (++nBandera);
      return '<svg viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice" aria-hidden="true">' +
        '<clipPath id="' + id + '"><path d="M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z"/></clipPath>' +
        '<rect width="60" height="30" fill="#012169"/>' +
        '<path d="M0,0 L60,30 M60,0 L0,30" stroke="#fff" stroke-width="6"/>' +
        '<path d="M0,0 L60,30 M60,0 L0,30" clip-path="url(#' + id + ')" stroke="#C8102E" stroke-width="4"/>' +
        '<path d="M30,0 v30 M0,15 h60" stroke="#fff" stroke-width="10"/>' +
        '<path d="M30,0 v30 M0,15 h60" stroke="#C8102E" stroke-width="6"/></svg>';
    },
    pt: () => '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#DA291C"/><rect width="12" height="20" fill="#046A38"/><circle cx="12" cy="10" r="4" fill="#FFE000"/><circle cx="12" cy="10" r="2.2" fill="#DA291C"/></svg>',
    fr: () => '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#fff"/><rect width="10" height="20" fill="#002654"/><rect x="20" width="10" height="20" fill="#CE1126"/></svg>'
  };

  const IDIOMAS = [
    { code: 'es', nombre: 'Español' },
    { code: 'gl', nombre: 'Galego' },
    { code: 'en', nombre: 'English' },
    { code: 'pt', nombre: 'Português' },
    { code: 'fr', nombre: 'Français' }
  ];

  const T = {
    es: {
      titulo_pagina: 'VigoVello · El Vigo de antes en el mapa',
      meta_desc: 'Mapa de fotografías históricas de Vigo: recorre la ciudad de antes calle a calle.',
      subtitulo: 'La ciudad de antes, en su sitio',
      epoca: 'Época', todas: 'Todas', sin_fecha: 'Sin fecha',
      decada: (d) => 'Años ' + d,
      acerca: 'Acerca de', idioma: 'Idioma',
      foto: 'foto', fotos: 'fotos', lugar: 'lugar', lugares: 'lugares',
      fotografia: 'fotografía', fotografias: 'fotografías',
      error_carga: 'No se pudieron cargar las fotos',
      mapa_aria: 'Mapa de Vigo con fotografías históricas',
      cerrar: 'Cerrar', anterior: 'Foto anterior', siguiente: 'Foto siguiente',
      lugar_sin_nombre: 'Lugar sin nombre', sin_titulo: 'Sin título',
      imagen_pendiente: 'Imagen pendiente',
      no_carga: 'No se pudo cargar', no_carga_det: 'La imagen no está disponible en su web de origen',
      ub_sin_confirmar: 'Ubicación sin confirmar · situada de forma orientativa',
      ub_aproximada: 'Ubicación aproximada',
      ub_sin_corta: 'ubicación sin confirmar',
      proponer: 'Proponer ubicación', proponer_otra: 'Proponer otra ubicación',
      ver_original: 'Ver en su web original',
      autor_desconocido: 'Autor desconocido',
      lic_PD: 'Dominio público', lic_PDM: 'Dominio público (Public Domain Mark)', lic_VER: 'Licencia: ver la ficha de origen',
      hacia: 'h.',
      prop_clic: (t) => 'Haz clic en el mapa donde crees que se tomó «' + t + '».',
      prop_marcado: 'Punto marcado. Puedes hacer clic en otro sitio para cambiarlo.',
      prop_comentario: 'Comentario (opcional): ¿qué te hace pensar que es aquí?',
      prop_nota: 'Se abrirá GitHub para enviar la propuesta (hace falta una cuenta gratuita). La revisaremos antes de cambiar el mapa.',
      cancelar: 'Cancelar', enviar: 'Enviar propuesta',
      ley_conocida: 'Ubicación conocida', ley_sin: 'Sin confirmar',
      acerca_titulo: 'Acerca de VigoVello',
      acerca_html:
        '<p>Un mapa de fotografías históricas de Vigo, inspirado en <a href="https://www.oldnyc.org" target="_blank" rel="noopener">OldNYC</a>. Cada punto del mapa es un lugar: púlsalo para ver las imágenes tomadas allí.</p>' +
        '<p>VigoVello no almacena ninguna fotografía: es un visor. Cada imagen se carga desde la web donde está alojada, que se indica junto a la foto con su autor y licencia. Solo se usan imágenes de dominio público o con licencia libre.</p>' +
        '<p>Las fotos con el punto hueco no tienen una ubicación confirmada. Si sabes dónde se tomaron, usa «Proponer ubicación» en la foto. También puedes <a id="enlace-repo" href="#" target="_blank" rel="noopener">colaborar en el proyecto</a>.</p>'
    },
    gl: {
      titulo_pagina: 'VigoVello · O Vigo de antes no mapa',
      meta_desc: 'Mapa de fotografías históricas de Vigo: percorre a cidade de antes rúa a rúa.',
      subtitulo: 'A cidade de antes, no seu sitio',
      epoca: 'Época', todas: 'Todas', sin_fecha: 'Sen data',
      decada: (d) => 'Anos ' + d,
      acerca: 'Acerca de', idioma: 'Idioma',
      foto: 'foto', fotos: 'fotos', lugar: 'lugar', lugares: 'lugares',
      fotografia: 'fotografía', fotografias: 'fotografías',
      error_carga: 'Non se puideron cargar as fotos',
      mapa_aria: 'Mapa de Vigo con fotografías históricas',
      cerrar: 'Pechar', anterior: 'Foto anterior', siguiente: 'Foto seguinte',
      lugar_sin_nombre: 'Lugar sen nome', sin_titulo: 'Sen título',
      imagen_pendiente: 'Imaxe pendente',
      no_carga: 'Non se puido cargar', no_carga_det: 'A imaxe non está dispoñible na súa web de orixe',
      ub_sin_confirmar: 'Localización sen confirmar · situada de xeito orientativo',
      ub_aproximada: 'Localización aproximada',
      ub_sin_corta: 'localización sen confirmar',
      proponer: 'Propoñer localización', proponer_otra: 'Propoñer outra localización',
      ver_original: 'Ver na súa web orixinal',
      autor_desconocido: 'Autor descoñecido',
      lic_PD: 'Dominio público', lic_PDM: 'Dominio público (Public Domain Mark)', lic_VER: 'Licenza: ver a ficha de orixe',
      hacia: 'c.',
      prop_clic: (t) => 'Fai clic no mapa onde cres que se tomou «' + t + '».',
      prop_marcado: 'Punto marcado. Podes facer clic noutro sitio para cambialo.',
      prop_comentario: 'Comentario (opcional): que che fai pensar que é aquí?',
      prop_nota: 'Abrirase GitHub para enviar a proposta (cómpre unha conta gratuíta). Revisarémola antes de cambiar o mapa.',
      cancelar: 'Cancelar', enviar: 'Enviar proposta',
      ley_conocida: 'Localización coñecida', ley_sin: 'Sen confirmar',
      acerca_titulo: 'Acerca de VigoVello',
      acerca_html:
        '<p>Un mapa de fotografías históricas de Vigo, inspirado en <a href="https://www.oldnyc.org" target="_blank" rel="noopener">OldNYC</a>. Cada punto do mapa é un lugar: prémeo para ver as imaxes tomadas alí.</p>' +
        '<p>VigoVello non almacena ningunha fotografía: é un visor. Cada imaxe cárgase dende a web onde está aloxada, que se indica xunto á foto co seu autor e licenza. Só se usan imaxes de dominio público ou con licenza libre.</p>' +
        '<p>As fotos co punto oco non teñen unha localización confirmada. Se sabes onde se tomaron, usa «Propoñer localización» na foto. Tamén podes <a id="enlace-repo" href="#" target="_blank" rel="noopener">colaborar no proxecto</a>.</p>'
    },
    en: {
      titulo_pagina: 'VigoVello · Old Vigo on the map',
      meta_desc: 'A map of historical photographs of Vigo: explore the old city street by street.',
      subtitulo: 'The city of old, in its place',
      epoca: 'Period', todas: 'All', sin_fecha: 'Undated',
      decada: (d) => d + 's',
      acerca: 'About', idioma: 'Language',
      foto: 'photo', fotos: 'photos', lugar: 'place', lugares: 'places',
      fotografia: 'photograph', fotografias: 'photographs',
      error_carga: 'The photos could not be loaded',
      mapa_aria: 'Map of Vigo with historical photographs',
      cerrar: 'Close', anterior: 'Previous photo', siguiente: 'Next photo',
      lugar_sin_nombre: 'Unnamed place', sin_titulo: 'Untitled',
      imagen_pendiente: 'Image pending',
      no_carga: 'Could not load', no_carga_det: 'The image is not available on its source website',
      ub_sin_confirmar: 'Location unconfirmed · placed approximately',
      ub_aproximada: 'Approximate location',
      ub_sin_corta: 'location unconfirmed',
      proponer: 'Suggest a location', proponer_otra: 'Suggest another location',
      ver_original: 'View on its original website',
      autor_desconocido: 'Unknown author',
      lic_PD: 'Public domain', lic_PDM: 'Public domain (Public Domain Mark)', lic_VER: 'Licence: see the source page',
      hacia: 'c.',
      prop_clic: (t) => 'Click on the map where you think “' + t + '” was taken.',
      prop_marcado: 'Point marked. You can click elsewhere to change it.',
      prop_comentario: 'Comment (optional): what makes you think it was here?',
      prop_nota: 'GitHub will open so you can send the suggestion (a free account is needed). We will review it before changing the map.',
      cancelar: 'Cancel', enviar: 'Send suggestion',
      ley_conocida: 'Known location', ley_sin: 'Unconfirmed',
      acerca_titulo: 'About VigoVello',
      acerca_html:
        '<p>A map of historical photographs of Vigo, inspired by <a href="https://www.oldnyc.org" target="_blank" rel="noopener">OldNYC</a>. Each point on the map is a place: click it to see the images taken there.</p>' +
        '<p>VigoVello does not store any photographs: it is a viewer. Each image is loaded from the website where it is hosted, shown next to the photo with its author and licence. Only public-domain or freely licensed images are used.</p>' +
        '<p>Photos with a hollow point do not have a confirmed location. If you know where they were taken, use “Suggest a location” on the photo. You can also <a id="enlace-repo" href="#" target="_blank" rel="noopener">contribute to the project</a>.</p>'
    },
    pt: {
      titulo_pagina: 'VigoVello · A Vigo de antigamente no mapa',
      meta_desc: 'Mapa de fotografias históricas de Vigo: percorra a cidade de antigamente rua a rua.',
      subtitulo: 'A cidade de antigamente, no seu lugar',
      epoca: 'Época', todas: 'Todas', sin_fecha: 'Sem data',
      decada: (d) => 'Anos ' + d,
      acerca: 'Sobre', idioma: 'Idioma',
      foto: 'foto', fotos: 'fotos', lugar: 'local', lugares: 'locais',
      fotografia: 'fotografia', fotografias: 'fotografias',
      error_carga: 'Não foi possível carregar as fotos',
      mapa_aria: 'Mapa de Vigo com fotografias históricas',
      cerrar: 'Fechar', anterior: 'Foto anterior', siguiente: 'Foto seguinte',
      lugar_sin_nombre: 'Local sem nome', sin_titulo: 'Sem título',
      imagen_pendiente: 'Imagem pendente',
      no_carga: 'Não foi possível carregar', no_carga_det: 'A imagem não está disponível no seu site de origem',
      ub_sin_confirmar: 'Localização por confirmar · situada de forma aproximada',
      ub_aproximada: 'Localização aproximada',
      ub_sin_corta: 'localização por confirmar',
      proponer: 'Sugerir localização', proponer_otra: 'Sugerir outra localização',
      ver_original: 'Ver no site original',
      autor_desconocido: 'Autor desconhecido',
      lic_PD: 'Domínio público', lic_PDM: 'Domínio público (Public Domain Mark)', lic_VER: 'Licença: ver a página de origem',
      hacia: 'c.',
      prop_clic: (t) => 'Clique no mapa onde acha que foi tirada «' + t + '».',
      prop_marcado: 'Ponto marcado. Pode clicar noutro sítio para o alterar.',
      prop_comentario: 'Comentário (opcional): o que o leva a pensar que é aqui?',
      prop_nota: 'O GitHub vai abrir para enviar a sugestão (é preciso uma conta gratuita). Vamos revê-la antes de alterar o mapa.',
      cancelar: 'Cancelar', enviar: 'Enviar sugestão',
      ley_conocida: 'Localização conhecida', ley_sin: 'Por confirmar',
      acerca_titulo: 'Sobre o VigoVello',
      acerca_html:
        '<p>Um mapa de fotografias históricas de Vigo, inspirado no <a href="https://www.oldnyc.org" target="_blank" rel="noopener">OldNYC</a>. Cada ponto do mapa é um local: clique nele para ver as imagens tiradas ali.</p>' +
        '<p>O VigoVello não armazena nenhuma fotografia: é um visualizador. Cada imagem é carregada a partir do site onde está alojada, indicado junto à foto com o seu autor e licença. Só se usam imagens de domínio público ou com licença livre.</p>' +
        '<p>As fotos com o ponto vazio não têm localização confirmada. Se sabe onde foram tiradas, use «Sugerir localização» na foto. Também pode <a id="enlace-repo" href="#" target="_blank" rel="noopener">colaborar no projeto</a>.</p>'
    },
    fr: {
      titulo_pagina: 'VigoVello · Le Vigo d’autrefois sur la carte',
      meta_desc: 'Carte de photographies historiques de Vigo : parcourez la ville d’autrefois rue par rue.',
      subtitulo: 'La ville d’autrefois, à sa place',
      epoca: 'Époque', todas: 'Toutes', sin_fecha: 'Sans date',
      decada: (d) => 'Années ' + d,
      acerca: 'À propos', idioma: 'Langue',
      foto: 'photo', fotos: 'photos', lugar: 'lieu', lugares: 'lieux',
      fotografia: 'photographie', fotografias: 'photographies',
      error_carga: 'Impossible de charger les photos',
      mapa_aria: 'Carte de Vigo avec des photographies historiques',
      cerrar: 'Fermer', anterior: 'Photo précédente', siguiente: 'Photo suivante',
      lugar_sin_nombre: 'Lieu sans nom', sin_titulo: 'Sans titre',
      imagen_pendiente: 'Image à venir',
      no_carga: 'Chargement impossible', no_carga_det: 'L’image n’est pas disponible sur son site d’origine',
      ub_sin_confirmar: 'Emplacement non confirmé · placé à titre indicatif',
      ub_aproximada: 'Emplacement approximatif',
      ub_sin_corta: 'emplacement non confirmé',
      proponer: 'Proposer un emplacement', proponer_otra: 'Proposer un autre emplacement',
      ver_original: 'Voir sur le site d’origine',
      autor_desconocido: 'Auteur inconnu',
      lic_PD: 'Domaine public', lic_PDM: 'Domaine public (Public Domain Mark)', lic_VER: 'Licence : voir la page d’origine',
      hacia: 'v.',
      prop_clic: (t) => 'Cliquez sur la carte là où vous pensez que « ' + t + ' » a été prise.',
      prop_marcado: 'Point placé. Vous pouvez cliquer ailleurs pour le déplacer.',
      prop_comentario: 'Commentaire (facultatif) : qu’est-ce qui vous fait penser que c’est ici ?',
      prop_nota: 'GitHub va s’ouvrir pour envoyer la proposition (un compte gratuit est nécessaire). Nous la vérifierons avant de modifier la carte.',
      cancelar: 'Annuler', enviar: 'Envoyer la proposition',
      ley_conocida: 'Emplacement connu', ley_sin: 'Non confirmé',
      acerca_titulo: 'À propos de VigoVello',
      acerca_html:
        '<p>Une carte de photographies historiques de Vigo, inspirée d’<a href="https://www.oldnyc.org" target="_blank" rel="noopener">OldNYC</a>. Chaque point de la carte est un lieu : cliquez dessus pour voir les images prises à cet endroit.</p>' +
        '<p>VigoVello ne stocke aucune photographie : c’est une visionneuse. Chaque image est chargée depuis le site qui l’héberge, indiqué à côté de la photo avec son auteur et sa licence. Seules des images du domaine public ou sous licence libre sont utilisées.</p>' +
        '<p>Les photos au point creux n’ont pas d’emplacement confirmé. Si vous savez où elles ont été prises, utilisez « Proposer un emplacement » sur la photo. Vous pouvez aussi <a id="enlace-repo" href="#" target="_blank" rel="noopener">contribuer au projet</a>.</p>'
    }
  };

  // Nombres de lugar genéricos. Los topónimos oficiales (Porta do Sol, O Berbés…) no se traducen.
  const LUGARES = {
    'Vigo (sin ubicar)': { es: 'Vigo (sin ubicar)', gl: 'Vigo (sen localizar)', en: 'Vigo (not located)', pt: 'Vigo (sem localização)', fr: 'Vigo (non localisé)' },
    'Ría de Vigo': { es: 'Ría de Vigo', gl: 'Ría de Vigo', en: 'Vigo estuary', pt: 'Ria de Vigo', fr: 'Ria de Vigo' },
    'Puerto de Vigo': { es: 'Puerto de Vigo', gl: 'Porto de Vigo', en: 'Port of Vigo', pt: 'Porto de Vigo', fr: 'Port de Vigo' },
    'Antigua playa del Areal': { es: 'Antigua playa del Areal', gl: 'Antiga praia do Areal', en: 'Former Areal beach', pt: 'Antiga praia do Areal', fr: 'Ancienne plage de l’Areal' },
    'Casa de Caridad': { es: 'Casa de Caridad', gl: 'Casa de Caridade', en: 'Charity House', pt: 'Casa de Caridade', fr: 'Maison de charité' },
    'Escuela Obrera': { es: 'Escuela Obrera', gl: 'Escola Obreira', en: 'Workers’ School', pt: 'Escola Operária', fr: 'École ouvrière' },
    'Vista general': { es: 'Vista general', gl: 'Vista xeral', en: 'General view', pt: 'Vista geral', fr: 'Vue générale' },
    'Vista general desde el Castro': { es: 'Vista general desde el Castro', gl: 'Vista xeral dende o Castro', en: 'General view from O Castro', pt: 'Vista geral do Castro', fr: 'Vue générale depuis le Castro' },
    'Muelle de Trasatlánticos': { es: 'Muelle de Trasatlánticos', gl: 'Peirao de Transatlánticos', en: 'Ocean liner pier', pt: 'Cais dos Transatlânticos', fr: 'Quai des transatlantiques' },
    'Teatro García Barbón': { es: 'Teatro García Barbón', gl: 'Teatro García Barbón', en: 'García Barbón Theatre', pt: 'Teatro García Barbón', fr: 'Théâtre García Barbón' },
    'Estación de ferrocarril': { es: 'Estación de ferrocarril', gl: 'Estación de ferrocarril', en: 'Railway station', pt: 'Estação ferroviária', fr: 'Gare ferroviaire' },
    'Real Club Náutico': { es: 'Real Club Náutico', gl: 'Real Club Náutico', en: 'Royal Yacht Club', pt: 'Real Clube Náutico', fr: 'Real Club Náutico' },
    'Casco Vello': { es: 'Casco Vello', gl: 'Casco Vello', en: 'Old Town (Casco Vello)', pt: 'Casco Vello (centro histórico)', fr: 'Vieille ville (Casco Vello)' },
    'Monte do Castro': { es: 'Monte do Castro', gl: 'Monte do Castro', en: 'O Castro hill', pt: 'Monte do Castro', fr: 'Colline du Castro' },
    'Illas Cíes': { es: 'Islas Cíes', gl: 'Illas Cíes', en: 'Cíes Islands', pt: 'Ilhas Cíes', fr: 'Îles Cíes' },
    'Praia de Samil': { es: 'Playa de Samil', gl: 'Praia de Samil', en: 'Samil beach', pt: 'Praia de Samil', fr: 'Plage de Samil' }
  };

  const CLAVE = 'vigovello-idioma';
  function inicial() {
    const q = new URLSearchParams(location.search).get('lang');
    if (q && T[q]) return q;
    try { const g = localStorage.getItem(CLAVE); if (g && T[g]) return g; } catch (e) {}
    for (const l of navigator.languages || [navigator.language || '']) {
      const c = String(l).slice(0, 2).toLowerCase();
      if (T[c]) return c;
    }
    return 'es';
  }

  let actual = inicial();
  const oyentes = [];

  window.I18N = {
    idiomas: IDIOMAS,
    bandera: (c) => BANDERAS[c](),
    get idioma() { return actual; },
    t(clave, ...args) {
      const v = (T[actual] && T[actual][clave]) ?? T.es[clave];
      return typeof v === 'function' ? v(...args) : v;
    },
    lugar(nombre) { return (LUGARES[nombre] && LUGARES[nombre][actual]) || nombre; },
    licencia(codigo) {
      if (!codigo) return '';
      const k = 'lic_' + codigo;
      return T[actual][k] || codigo;
    },
    plural(n, uno, varios) { return n + ' ' + (n === 1 ? this.t(uno) : this.t(varios)); },
    cambiar(c) {
      if (!T[c] || c === actual) return;
      actual = c;
      try { localStorage.setItem(CLAVE, c); } catch (e) {}
      oyentes.forEach((f) => f(c));
    },
    alCambiar(f) { oyentes.push(f); }
  };
})();
