(function () {
  'use strict';

  const C = window.CONFIG;
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
  L.tileLayer(C.teselas, { attribution: C.atribucion, maxZoom: C.zoomMax, className: 'teselas-gris' }).addTo(mapa);

  $('enlace-repo').href = C.repo;

  // ---------- Utilidades ----------
  const clave = (lat, lng) => lat.toFixed(5) + ',' + lng.toFixed(5);
  const decada = (anio) => (anio ? Math.floor(anio / 10) * 10 : null);

  function textoFecha(f) {
    if (f.fecha) return f.fecha;
    if (f.anio) return (f.aproximada ? 'h. ' : '') + f.anio;
    return 'Sin fecha';
  }

  function escapar(s) {
    return String(s ?? '').replace(/[&<>"']/g, (c) => (
      { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));
  }

  function imagenHTML(f, grande) {
    const src = grande ? (f.imagen || f.miniatura) : (f.miniatura || f.imagen);
    if (!src) {
      return '<div class="sin-imagen"><span>' + escapar(f.titulo) + '</span><small>Imagen pendiente</small></div>';
    }
    // La imagen se carga directamente desde la web donde está alojada; aquí no se guarda nada.
    // Si la versión reducida falla, se prueba con el archivo original antes de rendirse.
    const alt = f.original && f.original !== src ? ' data-original="' + escapar(f.original) + '"' : '';
    return '<img src="' + escapar(src) + '" alt="' + escapar(f.titulo) + '" loading="lazy" referrerpolicy="no-referrer"' +
      alt + ' onerror="vvFalloImagen(this)">';
  }

  window.vvFalloImagen = function (img) {
    const orig = img.getAttribute('data-original');
    if (orig) { img.removeAttribute('data-original'); img.src = orig; return; }
    img.outerHTML = '<div class="sin-imagen"><span>No se pudo cargar</span><small>La imagen no está disponible en su web de origen</small></div>';
  };

  const sinConfirmar = (f) => f.ubicacion === 'sin_confirmar';
  const TEXTO_UBICACION = {
    sin_confirmar: 'Ubicación sin confirmar · situada de forma orientativa',
    aproximada: 'Ubicación aproximada'
  };

  // ---------- Datos ----------
  fetch(C.datos)
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((datos) => {
      fotos = (datos.fotos || datos).filter((f) => typeof f.lat === 'number' && typeof f.lng === 'number');
      prepararFiltro();
      pintar();
      leerEnlace();
    })
    .catch((e) => {
      $('contador').textContent = 'No se pudieron cargar las fotos';
      console.error('Error cargando', C.datos, e);
    });

  function prepararFiltro() {
    const decadas = [...new Set(fotos.map((f) => decada(f.anio)).filter(Boolean))].sort();
    const sel = $('filtro-decada');
    decadas.forEach((d) => {
      const o = document.createElement('option');
      o.value = d;
      o.textContent = 'Años ' + String(d).slice(-2) + ' (' + d + 's)';
      sel.appendChild(o);
    });
    if (fotos.some((f) => !f.anio)) {
      const o = document.createElement('option');
      o.value = 'sin';
      o.textContent = 'Sin fecha';
      sel.appendChild(o);
    }
    sel.addEventListener('change', () => { cerrarPanel(); pintar(); });
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
      m.bindTooltip((l.nombre || 'Lugar') + ' · ' + n + (n === 1 ? ' foto' : ' fotos') +
        (l.sinConfirmar ? ' · ubicación sin confirmar' : ''), { direction: 'top', offset: [0, -6] });
      m.on('click', () => abrirLugar(k));
      m.addTo(capaPuntos);
    });
    capaPuntos.addTo(mapa);

    const total = fotosFiltradas().length;
    $('contador').textContent = total + (total === 1 ? ' foto' : ' fotos') + ' · ' + lugares.size + (lugares.size === 1 ? ' lugar' : ' lugares');
  }

  // ---------- Panel de un lugar ----------
  function abrirLugar(k, sinHistorial) {
    const l = lugares.get(k);
    if (!l) return;
    lugarAbierto = k;
    $('panel-titulo').textContent = l.nombre || 'Lugar sin nombre';
    const anios = l.fotos.map((f) => f.anio).filter(Boolean);
    const rango = anios.length ? (Math.min(...anios) === Math.max(...anios) ? Math.min(...anios) : Math.min(...anios) + '–' + Math.max(...anios)) : '';
    $('panel-resumen').textContent = l.fotos.length + (l.fotos.length === 1 ? ' fotografía' : ' fotografías') + (rango ? ' · ' + rango : '') +
      (l.sinConfirmar ? ' · ubicación sin confirmar' : '');

    const ul = $('panel-rejilla');
    ul.innerHTML = '';
    l.fotos.forEach((f, i) => {
      const li = document.createElement('li');
      li.innerHTML =
        '<button type="button" class="miniatura">' + imagenHTML(f, false) +
        '<span class="pie">' + escapar(textoFecha(f)) + '</span></button>';
      li.querySelector('button').addEventListener('click', () => abrirVisor(l.fotos, i));
      ul.appendChild(li);
    });

    $('panel').hidden = false;
    document.body.classList.add('con-panel');
    mapa.panTo([l.lat, l.lng], { animate: true });
    if (!sinHistorial) history.replaceState(null, '', '#lugar=' + k);
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
    $('visor-imagen').innerHTML = imagenHTML(f, true);
    $('visor-titulo').textContent = f.titulo || 'Sin título';
    $('visor-meta').textContent = [textoFecha(f), f.lugar].filter(Boolean).join(' · ');
    $('visor-desc').textContent = f.descripcion || '';
    const avisoUb = TEXTO_UBICACION[f.ubicacion];
    $('visor-ubicacion').hidden = !avisoUb;
    $('visor-ubicacion').textContent = avisoUb || '';
    $('btn-proponer').textContent = sinConfirmar(f) ? 'Proponer ubicación' : 'Proponer otra ubicación';

    const partes = [];
    if (f.autor) partes.push(escapar(f.autor));
    if (f.fuente) partes.push(f.url_fuente
      ? '<a href="' + escapar(f.url_fuente) + '" target="_blank" rel="noopener">' + escapar(f.fuente) + '</a>'
      : escapar(f.fuente));
    if (f.licencia) partes.push(escapar(f.licencia));
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
  let propuesta = null; // { foto, latlng }
  const capaPropuesta = L.layerGroup().addTo(mapa);

  function iniciarPropuesta() {
    const f = fotosVisor[indiceVisor];
    propuesta = { foto: f, latlng: null };
    cerrarCapa('visor');
    cerrarPanel();
    capaPropuesta.clearLayers();
    $('propuesta-texto').textContent = 'Haz clic en el mapa donde crees que se tomó «' + (f.titulo || 'esta foto') + '».';
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
    $('propuesta-texto').textContent = 'Punto marcado. Puedes hacer clic en otro sitio para cambiarlo.';
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
    if (!$('visor').hidden) {
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
        const k = clave(f.lat, f.lng);
        mapa.setView([f.lat, f.lng], Math.max(mapa.getZoom(), 16));
        abrirLugar(k, true);
        const l = lugares.get(k);
        abrirVisor(l.fotos, l.fotos.indexOf(f));
      }
    }
  }
})();
