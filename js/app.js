(function () {
  'use strict';

  const C = window.CONFIG;
  const I = window.I18N;
  const t = (...a) => I.t(...a);
  const $ = (id) => document.getElementById(id);

  let fotos = [];          // todas las fotos
  let lugares = new Map(); // clave "lat,lng" -> { lat, lng, nombre, fotos[] }
  let capaPuntos = null;
  let lugarAbierto = null; // clave del lugar abierto en el panel
  let fotosVisor = [];     // fotos que recorre el visor
  let indiceVisor = 0;

  // ---------- Mapa ----------
  const mapa = L.map('mapa', {
    center: C.centro,
    zoom: C.zoom,
    minZoom: C.zoomMin,
    maxZoom: C.zoomMax,
    zoomControl: false
  });
  L.control.zoom({ position: 'bottomright' }).addTo(mapa);
  L.tileLayer(C.teselas, { attribution: C.atribucion, maxZoom: C.zoomMax, className: 'teselas-oscuras' }).addTo(mapa);

  // ---------- Utilidades ----------
  const clave = (lat, lng) => lat.toFixed(5) + ',' + lng.toFixed(5);
  const decada = (anio) => (anio ? Math.floor(anio / 10) * 10 : null);
  const sinConfirmar = (f) => f.ubicacion === 'sin_confirmar';

  // Textos de una foto en el idioma actual (con el español como respaldo)
  function txt(f) {
    const x = (f.textos && (f.textos[I.idioma] || f.textos.es)) || {};
    return { titulo: x.titulo || f.titulo || t('sin_titulo'), descripcion: x.descripcion ?? f.descripcion ?? '' };
  }

  function textoFecha(f) {
    if (f.anio) return (f.aproximada ? t('hacia') + ' ' : '') + f.anio;
    return t('sin_fecha');
  }

  function escapar(s) {
    return String(s ?? '').replace(/[&<>"']/g, (c) => (
      { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));
  }

  function imagenHTML(f, grande) {
    const src = grande ? (f.imagen || f.miniatura) : (f.miniatura || f.imagen);
    if (!src) {
      return '<div class="sin-imagen"><span>' + escapar(txt(f).titulo) + '</span><small>' + escapar(t('imagen_pendiente')) + '</small></div>';
    }
    // La imagen se carga directamente desde la web donde está alojada; aquí no se guarda nada.
    // Si la versión reducida falla, se prueba con el archivo original antes de rendirse.
    const alt = f.original && f.original !== src ? ' data-original="' + escapar(f.original) + '"' : '';
    return '<img src="' + escapar(src) + '" alt="' + escapar(txt(f).titulo) + '" loading="lazy" referrerpolicy="no-referrer"' +
      alt + ' onerror="vvFalloImagen(this)">';
  }

  window.vvFalloImagen = function (img) {
    const orig = img.getAttribute('data-original');
    if (orig) { img.removeAttribute('data-original'); img.src = orig; return; }
    img.outerHTML = '<div class="sin-imagen"><span>' + escapar(t('no_carga')) + '</span><small>' + escapar(t('no_carga_det')) + '</small></div>';
  };

  // ---------- Textos fijos de la página ----------
  function aplicarTextos() {
    document.documentElement.lang = I.idioma;
    document.title = t('titulo_pagina');
    document.querySelector('meta[name="description"]').content = t('meta_desc');
    document.querySelectorAll('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });
    document.querySelectorAll('[data-i18n-aria]').forEach((el) => { el.setAttribute('aria-label', t(el.dataset.i18nAria)); });
    $('acerca-cuerpo').innerHTML = t('acerca_html');
    $('enlace-repo').href = C.repo;
    $('idioma-bandera').innerHTML = I.bandera(I.idioma);
    $('idioma-codigo').textContent = I.idioma.toUpperCase();
    $('btn-idioma').setAttribute('aria-label', t('idioma'));
    pintarMenuIdioma();
  }

  // ---------- Selector de idioma ----------
  function pintarMenuIdioma() {
    const ul = $('menu-idioma');
    ul.innerHTML = '';
    I.idiomas.forEach((l) => {
      const li = document.createElement('li');
      li.setAttribute('role', 'none');
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'menuitemradio');
      b.setAttribute('aria-checked', String(l.code === I.idioma));
      b.lang = l.code;
      b.innerHTML = '<span class="bandera">' + I.bandera(l.code) + '</span><span>' + l.nombre + '</span>';
      b.addEventListener('click', () => { cerrarMenuIdioma(); I.cambiar(l.code); });
      li.appendChild(b);
      ul.appendChild(li);
    });
  }
  function abrirMenuIdioma() {
    $('menu-idioma').hidden = false;
    $('btn-idioma').setAttribute('aria-expanded', 'true');
    const sel = $('menu-idioma').querySelector('[aria-checked="true"]');
    if (sel) sel.focus();
  }
  function cerrarMenuIdioma() {
    $('menu-idioma').hidden = true;
    $('btn-idioma').setAttribute('aria-expanded', 'false');
  }
  $('btn-idioma').addEventListener('click', (e) => {
    e.stopPropagation();
    $('menu-idioma').hidden ? abrirMenuIdioma() : cerrarMenuIdioma();
  });
  document.addEventListener('click', (e) => {
    if (!$('menu-idioma').hidden && !e.target.closest('.idioma')) cerrarMenuIdioma();
  });

  I.alCambiar(() => {
    aplicarTextos();
    prepararFiltro();
    pintar();
    if (lugarAbierto && lugares.has(lugarAbierto)) abrirLugar(lugarAbierto, true);
    if (!$('visor').hidden) mostrarFoto();
    if (propuesta) $('propuesta-texto').textContent = propuesta.latlng ? t('prop_marcado') : t('prop_clic', txt(propuesta.foto).titulo);
  });

  aplicarTextos();

  // ---------- Datos ----------
  fetch(C.datos)
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((datos) => {
      fotos = (datos.fotos || datos).filter((f) => typeof f.lat === 'number' && typeof f.lng === 'number');
      prepararFiltro();
      $('filtro-decada').addEventListener('change', () => { cerrarPanel(); pintar(); });
      pintar();
      leerEnlace();
    })
    .catch((e) => {
      $('contador').textContent = t('error_carga');
      console.error('Error cargando', C.datos, e);
    });

  function prepararFiltro() {
    const sel = $('filtro-decada');
    const valor = sel.value;
    sel.innerHTML = '';
    const add = (v, texto) => { const o = document.createElement('option'); o.value = v; o.textContent = texto; sel.appendChild(o); };
    add('', t('todas'));
    [...new Set(fotos.map((f) => decada(f.anio)).filter(Boolean))].sort().forEach((d) => add(d, t('decada', d)));
    if (fotos.some((f) => !f.anio)) add('sin', t('sin_fecha'));
    sel.value = valor;
    if (sel.selectedIndex < 0) sel.value = '';
  }

  function fotosFiltradas() {
    const v = $('filtro-decada').value;
    if (!v) return fotos;
    if (v === 'sin') return fotos.filter((f) => !f.anio);
    return fotos.filter((f) => decada(f.anio) === Number(v));
  }

  function pintar() {
    if (capaPuntos) capaPuntos.remove();
    lugares = new Map();

    fotosFiltradas().forEach((f) => {
      const k = clave(f.lat, f.lng);
      if (!lugares.has(k)) lugares.set(k, { lat: f.lat, lng: f.lng, nombre: f.lugar || '', fotos: [] });
      const l = lugares.get(k);
      l.fotos.push(f);
      if (!l.nombre && f.lugar) l.nombre = f.lugar;
    });

    capaPuntos = L.layerGroup();
    lugares.forEach((l, k) => {
      l.fotos.sort((a, b) => (a.anio || 9999) - (b.anio || 9999));
      const n = l.fotos.length;
      l.sinConfirmar = l.fotos.every(sinConfirmar);
      const m = L.circleMarker([l.lat, l.lng], {
        radius: 6 + Math.min(10, Math.sqrt(n) * 2),
        className: 'punto' + (l.sinConfirmar ? ' punto-sin-confirmar' : ''),
        weight: 1.5
      });
      m.bindTooltip((l.nombre ? I.lugar(l.nombre) : t('lugar_sin_nombre')) + ' · ' + I.plural(n, 'foto', 'fotos') +
        (l.sinConfirmar ? ' · ' + t('ub_sin_corta') : ''), { direction: 'top', offset: [0, -6] });
      m.on('click', () => abrirLugar(k));
      m.addTo(capaPuntos);
    });
    capaPuntos.addTo(mapa);

    const total = fotosFiltradas().length;
    $('contador').textContent = I.plural(total, 'foto', 'fotos') + ' · ' + I.plural(lugares.size, 'lugar', 'lugares');
  }

  // ---------- Panel de un lugar ----------
  function abrirLugar(k, sinHistorial) {
    const l = lugares.get(k);
    if (!l) return;
    lugarAbierto = k;
    $('panel-titulo').textContent = l.nombre ? I.lugar(l.nombre) : t('lugar_sin_nombre');
    const anios = l.fotos.map((f) => f.anio).filter(Boolean);
    const rango = anios.length ? (Math.min(...anios) === Math.max(...anios) ? Math.min(...anios) : Math.min(...anios) + '–' + Math.max(...anios)) : '';
    $('panel-resumen').textContent = I.plural(l.fotos.length, 'fotografia', 'fotografias') + (rango ? ' · ' + rango : '') +
      (l.sinConfirmar ? ' · ' + t('ub_sin_corta') : '');

    const ul = $('panel-rejilla');
    ul.innerHTML = '';
    l.fotos.forEach((f, i) => {
      const li = document.createElement('li');
      li.innerHTML =
        '<button type="button" class="miniatura" title="' + escapar(txt(f).titulo) + '">' + imagenHTML(f, false) +
        '<span class="pie">' + escapar(textoFecha(f)) + '</span></button>';
      li.querySelector('button').addEventListener('click', () => abrirVisor(l.fotos, i));
      ul.appendChild(li);
    });

    $('panel').hidden = false;
    document.body.classList.add('con-panel');
    if (!sinHistorial) {
      mapa.panTo([l.lat, l.lng], { animate: true });
      history.replaceState(null, '', '#lugar=' + k);
    }
  }

  function cerrarPanel() {
    $('panel').hidden = true;
    document.body.classList.remove('con-panel');
    lugarAbierto = null;
    history.replaceState(null, '', location.pathname + location.search);
  }
  $('panel-cerrar').addEventListener('click', cerrarPanel);

  // ---------- Visor ----------
  function abrirVisor(lista, i) {
    fotosVisor = lista;
    indiceVisor = i;
    mostrarFoto();
    $('visor').hidden = false;
    document.querySelector('#visor .capa-cerrar').focus();
  }

  function mostrarFoto() {
    const f = fotosVisor[indiceVisor];
    const x = txt(f);
    $('visor-imagen').innerHTML = imagenHTML(f, true);
    $('visor-titulo').textContent = x.titulo;
    $('visor-meta').textContent = [textoFecha(f), f.lugar ? I.lugar(f.lugar) : ''].filter(Boolean).join(' · ');
    $('visor-desc').textContent = x.descripcion;
    $('visor-desc').hidden = !x.descripcion;

    const aviso = f.ubicacion === 'sin_confirmar' ? t('ub_sin_confirmar') : f.ubicacion === 'aproximada' ? t('ub_aproximada') : '';
    $('visor-ubicacion').hidden = !aviso;
    $('visor-ubicacion').textContent = aviso;
    $('btn-proponer').textContent = sinConfirmar(f) ? t('proponer') : t('proponer_otra');

    const partes = [escapar(f.autor || t('autor_desconocido'))];
    if (f.fuente) partes.push(f.url_fuente
      ? '<a href="' + escapar(f.url_fuente) + '" target="_blank" rel="noopener">' + escapar(f.fuente) + '</a>'
      : escapar(f.fuente));
    if (f.licencia) partes.push(escapar(I.licencia(f.licencia)));
    $('visor-credito').innerHTML = partes.join(' · ');

    const origen = f.url_fuente || f.imagen;
    $('visor-origen').hidden = !origen;
    if (origen) $('visor-origen').href = origen;

    const varias = fotosVisor.length > 1;
    document.querySelector('.visor-ant').hidden = !varias;
    document.querySelector('.visor-sig').hidden = !varias;
    if (f.id) history.replaceState(null, '', '#foto=' + encodeURIComponent(f.id));
  }

  function moverVisor(d) {
    indiceVisor = (indiceVisor + d + fotosVisor.length) % fotosVisor.length;
    mostrarFoto();
  }

  function cerrarCapa(id) {
    $(id).hidden = true;
    if (id === 'visor') {
      history.replaceState(null, '', lugarAbierto ? '#lugar=' + lugarAbierto : location.pathname + location.search);
    }
  }

  // ---------- Propuestas de ubicación ----------
  // El visitante marca un punto y se abre una propuesta (issue) en GitHub para validarla.
  // El texto de la propuesta va siempre en español: lo leen los responsables del proyecto.
  let propuesta = null; // { foto, latlng }
  const capaPropuesta = L.layerGroup().addTo(mapa);

  function iniciarPropuesta() {
    const f = fotosVisor[indiceVisor];
    propuesta = { foto: f, latlng: null };
    cerrarCapa('visor');
    cerrarPanel();
    capaPropuesta.clearLayers();
    $('propuesta-texto').textContent = t('prop_clic', txt(f).titulo);
    $('propuesta-detalle').hidden = true;
    $('propuesta').hidden = false;
    document.body.classList.add('proponiendo');
  }

  function terminarPropuesta() {
    propuesta = null;
    capaPropuesta.clearLayers();
    $('propuesta').hidden = true;
    $('propuesta-comentario').value = '';
    document.body.classList.remove('proponiendo');
  }

  mapa.on('click', (e) => {
    if (!propuesta) return;
    propuesta.latlng = { lat: +e.latlng.lat.toFixed(6), lng: +e.latlng.lng.toFixed(6) };
    capaPropuesta.clearLayers();
    L.circleMarker([propuesta.latlng.lat, propuesta.latlng.lng], { radius: 9, className: 'punto-propuesta', weight: 2 }).addTo(capaPropuesta);
    $('propuesta-texto').textContent = t('prop_marcado');
    $('propuesta-detalle').hidden = false;
  });

  function enviarPropuesta() {
    if (!propuesta || !propuesta.latlng) return;
    const f = propuesta.foto, p = propuesta.latlng;
    const cuerpo = [
      '**Foto:** ' + (f.titulo || '') + ' (`' + f.id + '`)',
      '**Ubicación actual:** ' + f.lat + ', ' + f.lng + (f.ubicacion === 'sin_confirmar' ? ' (sin confirmar)' : ''),
      '**Ubicación propuesta:** ' + p.lat + ', ' + p.lng,
      '',
      'Ver en el mapa: https://www.openstreetmap.org/?mlat=' + p.lat + '&mlon=' + p.lng + '#map=18/' + p.lat + '/' + p.lng,
      'Foto en VigoVello: ' + location.origin + location.pathname + '#foto=' + encodeURIComponent(f.id),
      f.url_fuente ? 'Ficha original: ' + f.url_fuente : '',
      'Idioma del visitante: ' + I.idioma,
      '',
      '**Comentario:**',
      $('propuesta-comentario').value.trim() || '(sin comentario)'
    ].join('\n');
    const url = C.repo + '/issues/new?title=' + encodeURIComponent('Ubicación: ' + (f.titulo || f.id)) +
      '&body=' + encodeURIComponent(cuerpo);
    window.open(url, '_blank', 'noopener');
    terminarPropuesta();
  }

  $('btn-proponer').addEventListener('click', iniciarPropuesta);
  $('propuesta-enviar').addEventListener('click', enviarPropuesta);
  $('propuesta-cancelar').addEventListener('click', terminarPropuesta);

  document.querySelector('.visor-ant').addEventListener('click', () => moverVisor(-1));
  document.querySelector('.visor-sig').addEventListener('click', () => moverVisor(1));
  document.querySelectorAll('[data-cerrar]').forEach((el) =>
    el.addEventListener('click', () => cerrarCapa(el.closest('.capa').id)));

  $('btn-acerca').addEventListener('click', () => { $('acerca').hidden = false; });

  document.addEventListener('keydown', (e) => {
    if (!$('menu-idioma').hidden && e.key === 'Escape') {
      cerrarMenuIdioma();
      $('btn-idioma').focus();
    } else if (!$('visor').hidden) {
      if (e.key === 'ArrowLeft') moverVisor(-1);
      else if (e.key === 'ArrowRight') moverVisor(1);
      else if (e.key === 'Escape') cerrarCapa('visor');
    } else if (!$('acerca').hidden && e.key === 'Escape') {
      cerrarCapa('acerca');
    } else if (propuesta && e.key === 'Escape') {
      terminarPropuesta();
    } else if (!$('panel').hidden && e.key === 'Escape') {
      cerrarPanel();
    }
  });

  // ---------- Enlaces directos (#lugar=… / #foto=…) ----------
  window.addEventListener('hashchange', () => { if (fotos.length) leerEnlace(); });
  function leerEnlace() {
    const h = decodeURIComponent(location.hash.slice(1));
    if (h.startsWith('lugar=')) {
      const k = h.slice(6);
      if (lugares.has(k)) {
        const l = lugares.get(k);
        mapa.setView([l.lat, l.lng], Math.max(mapa.getZoom(), 16));
        abrirLugar(k, true);
      }
    } else if (h.startsWith('foto=')) {
      const f = fotos.find((x) => String(x.id) === h.slice(5));
      if (f) {
        $('filtro-decada').value = '';
        pintar();
        const k = clave(f.lat, f.lng);
        mapa.setView([f.lat, f.lng], Math.max(mapa.getZoom(), 16));
        abrirLugar(k, true);
        const l = lugares.get(k);
        abrirVisor(l.fotos, l.fotos.indexOf(f));
      }
    }
  }
})();
