"use strict";
// Corredor Quebrada–Puna — offline dashboard. Data comes only from the embedded bundle and
// is rendered with textContent only (no HTML parsing of data, no document writes).
(function () {
  const D = JSON.parse(document.getElementById("datos").textContent);
  const SVG = "http://www.w3.org/2000/svg"; // namespace identifier, not a network resource
  const vista = document.getElementById("vista");

  const ESTADO = {
    alerta: "Alerta",
    sin_alerta: "Sin alerta",
    pendiente: "Umbral pendiente de definición",
    sin_datos: "Sin datos de pronóstico",
    no_comparable: "No comparable (modelo distinto)",
  };
  const CAUSA = { aluvion: "Aluvión", crecida: "Crecida", nieve: "Nieve", accidente: "Accidente",
    protesta: "Protesta", obra: "Obra", otro: "Otro" };
  const RUTA = { RN9: "RN 9", RN52: "RN 52", otra: "Otra" };
  const VAR = {
    lluvia_24h_mm: "Lluvia 24 h", lluvia_48h_mm: "Lluvia 48 h", lluvia_72h_mm: "Lluvia 72 h",
    lluvia_7d_mm: "Lluvia 7 días", lluvia_max_horaria_24h_mm: "Lluvia máx. horaria 24 h",
    lluvia_max_horaria_72h_mm: "Lluvia máx. horaria 72 h", nieve_24h_cm: "Nieve 24 h",
    nieve_72h_cm: "Nieve 72 h", nieve_7d_cm: "Nieve 7 días",
  };
  const HORIZ = { hoy: "Hoy (hasta ahora)", "24h": "Próximas 24 h", "72h": "Próximas 72 h" };
  const JAMA = { mop_cl: "MOP Chile (lado chileno)", argentina_gob_ar: "argentina.gob.ar (lado argentino)" };
  const CAMPO = {
    id: "Identificador", nombre_paso: "Paso", estado_prioridad: "Estado del paso", estado_vialidad: "Estado de la ruta",
    fecha_schema: "Horario de atención", fecha_schema_cancilleria: "Horario (Cancillería)", fecha_hora_consulta: "Consultado",
    OBJECTID: "Identificador", TRANSITABILIDAD: "Transitabilidad", ESTADOTIEMPO: "Tiempo", ESTADOCALZADA: "Calzada",
    CADENAS: "Cadenas", RESTRICCIONES: "Restricciones", HABILITADO: "Habilitado", ESTADOINFORME: "Informe",
    FECHA: "Fecha del informe", HORA: "Hora del informe", ADESDE: "Abierto desde", AHASTA: "Abierto hasta",
  };
  const DIAS = { Mo: "lun", Tu: "mar", We: "mié", Th: "jue", Fr: "vie", Sa: "sáb", Su: "dom" };
  function valorJama(v) {
    if (v === null || v === undefined) return "sin dato";
    return String(v).replace(/\b(Mo|Tu|We|Th|Fr|Sa|Su)\b/g, (d) => DIAS[d]).replace(/(\p{L}{3})-(\p{L}{3})/gu, "$1 a $2");
  }
  function tablaJama(rec) {
    return el("table", { class: "tabla" }, el("tbody", {}, ...Object.entries(rec).map(([k, v]) =>
      el("tr", {}, el("td", {}, CAMPO[k] || k), el("td", {}, valorJama(v))))));
  }
  const COLOR = { alerta: "#b00020", sin_alerta: "#1b6e35" };
  const ORDEN = ["alerta", "sin_datos", "sin_alerta", "no_comparable"];

  function el(tag, attrs, ...kids) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === "class") n.className = v; else n.setAttribute(k, v);
    }
    for (const k of kids) if (k !== null && k !== undefined) n.append(k instanceof Node ? k : String(k));
    return n;
  }
  function svg(tag, attrs) {
    const n = document.createElementNS(SVG, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, String(v));
    return n;
  }
  function safeHref(u) { return /^https?:\/\//i.test(String(u || "")) ? String(u) : null; }
  function link(text, url) {
    const h = safeHref(url);
    return h ? el("a", { href: h, rel: "noopener noreferrer", target: "_blank" }, text) : el("span", {}, text);
  }
  function num(v, unit) { return v === null || v === undefined ? "sin dato" : `${v} ${unit}`; }
  function unidad(f) { return f.endsWith("_cm") ? "cm" : "mm"; }
  function chip(estado) { return el("span", { class: "est est-" + estado }, ESTADO[estado] || estado); }
  function nombrePunto(id) { const p = D.puntos.find((x) => x.id === id); return p ? p.nombre : id; }

  function estadoPunto(p) {
    if (!D.umbrales.length) return "pendiente";
    if (!p.pronostico) return "sin_datos";
    const es = Object.values(p.pronostico.horizontes).map((h) => h.estado);
    return ORDEN.find((e) => es.includes(e)) || "sin_datos";
  }

  // ------------------------------------------------------------------ Mapa
  function vistaMapa() {
    const m = D.mapa;
    const pad = 40;
    const s = svg("svg", { viewBox: `${-pad} ${-pad} ${m.ancho + 2 * pad} ${m.alto + 2 * pad}`,
      class: "mapa", role: "img", "aria-label": "Mapa del corredor" });
    for (const l of m.lineas) {
      const tren = l.capa === "ferrocarril";
      s.append(svg("path", { d: l.d, fill: "none", stroke: tren ? "#7a4b00" : "#222",
        "stroke-width": tren ? 3 : 6, "stroke-dasharray": tren ? "10 7" : "none" }));
    }
    for (const g of m.lugares.filter((x) => x.capa === "contexto")) {
      s.append(svg("rect", { x: g.x - 6, y: g.y - 6, width: 12, height: 12,
        fill: g.tipo === "litio" ? "#5a2d82" : "#7a4b00" }));
    }
    for (const g of m.lugares.filter((x) => x.capa === "puntos")) {
      const p = D.puntos.find((x) => x.id === g.id);
      if (!p) continue;
      const e = estadoPunto(p);
      const a = svg("a", { href: "#punto/" + p.id });
      const c = svg("circle", { cx: g.x, cy: g.y, r: 17, fill: COLOR[e] || "#9a9a9a", stroke: "#111", "stroke-width": 4 });
      const t = svg("title", {}); t.textContent = `${p.nombre}: ${ESTADO[e]}`;
      c.append(t); a.append(c); s.append(a);
    }
    const leg = el("div", { class: "leyenda" },
      ...[["#b00020", "Alerta"], ["#1b6e35", "Sin alerta"], ["#9a9a9a", "Pendiente / sin datos"]].map(
        ([c, t]) => { const k = el("span", {}, el("i", { class: "chip" }), t); k.firstChild.style.background = c; return k; }),
      el("span", {}, "━ Ruta"), el("span", {}, "┅ Tren Solar"), el("span", {}, "■ Estación / litio"));
    const lista = el("ul", { class: "lista" }, ...D.puntos.map((p) => el("li", {},
      el("a", { class: "btn", href: "#punto/" + p.id }, el("span", {}, `${p.nombre} · ${RUTA[p.ruta]}`), chip(estadoPunto(p))))));
    const avisos = [];
    if (!D.umbrales.length) avisos.push(el("p", { class: "aviso" },
      "Umbral pendiente de definición: todavía no se eligieron umbrales, así que no se muestra ningún color de riesgo."));
    return [el("h2", {}, "Mapa"), ...avisos, s, el("p", { class: "muted" }, link(m.atribucion.nombre, m.atribucion.url)),
      leg, el("h3", {}, "Puntos críticos"), lista];
  }

  // ------------------------------------------------------------------ Ficha
  function eventoItem(e, conPunto) {
    const lugar = conPunto && e.punto_id ? " · " + nombrePunto(e.punto_id) : "";
    return el("div", { class: "evento" },
      el("div", { class: "meta" }, `${e.fecha} · ${RUTA[e.ruta]}${lugar} · ${CAUSA[e.causa] || e.causa} · ${e.n_medios} medio(s)` +
        (e.estable ? "" : " · solo fuentes nuevas")),
      e.notas ? el("div", { class: "muted" }, e.notas) : null,
      ...e.notas_medios.map((n) => el("div", {}, el("strong", {}, n.medio + ": "), link(n.titular, n.url))));
  }
  function vistaPunto(id) {
    const p = D.puntos.find((x) => x.id === id);
    if (!p) return [el("p", {}, "Punto desconocido.")];
    const out = [el("h2", {}, p.nombre),
      el("p", {}, `${RUTA[p.ruta]} · km ${p.km === null ? "sin dato" : p.km}` + (p.verificado ? " · verificado en OSM" : " · ubicación NO verificada")),
      p.nota_geo ? el("p", { class: "muted" }, p.nota_geo) : null];
    const c = p.celda;
    out.push(el("p", {}, !c ? "Celda ERA5: sin dato." : c.comparte_con.length
      ? `Comparte la celda ERA5 con: ${c.comparte_con.map(nombrePunto).join(", ")} (misma serie histórica de lluvia).`
      : "No comparte la celda ERA5 con otro punto."));
    if (c && c.diferencia_m !== null) out.push(el("p", { class: "muted" },
      `La celda ERA5 está ${Math.abs(c.diferencia_m)} m ${c.diferencia_m >= 0 ? "por encima" : "por debajo"} del punto: su lluvia no es la del lugar.`));
    out.push(el("h3", {}, "Riesgo"));
    const fc = p.pronostico;
    if (!fc) out.push(el("p", { class: "aviso" }, "Pronóstico no disponible en este paquete."));
    else {
      if (fc.error) out.push(el("p", { class: "aviso" }, fc.error));
      const hs = Object.keys(HORIZ);
      for (const h of hs) {
        const H = fc.horizontes[h];
        if (!H) continue;
        out.push(el("p", {}, el("strong", {}, `${HORIZ[h]} (ventana hasta ${H.hasta}): `), chip(H.estado)));
        for (const ev of H.evaluaciones) out.push(el("p", { class: "muted" },
          `${ev.grupo}: ${VAR[ev.variable.replace(/_pct$/, "")] || ev.variable} ≥ ${ev.umbral} ${ev.unidad} → ${ESTADO[ev.estado]}` +
          ` (valor ${num(ev.valor, unidad(ev.variable.replace(/_pct$/, "")))}, percentil ${ev.percentil === null ? "sin dato" : ev.percentil})`));
      }
      const head = el("tr", {}, el("th", {}, "Variable"), ...hs.map((h) => el("th", {}, HORIZ[h])));
      const rows = Object.keys(VAR).map((f) => el("tr", {}, el("td", {}, `${VAR[f]} (${unidad(f)})`),
        ...hs.map((h) => { const v = fc.horizontes[h] && fc.horizontes[h].variables[f];
          return el("td", {}, !v || v.valor === null ? "sin dato" : `${v.valor} · p${v.percentil === null ? "?" : v.percentil}`); })));
      out.push(el("table", { class: "tabla" }, el("thead", {}, head), el("tbody", {}, ...rows)));
      out.push(el("p", { class: "muted" }, `Valor del pronóstico (${D.encabezado.pronostico_modelo}) y su percentil en la climatología del MISMO modelo ` +
        `(${fc.clima_desde || "sin dato"} → ${fc.clima_hasta || "sin dato"}, misma estación). p? = sin climatología.`));
    }
    const evs = D.eventos.filter((e) => e.punto_id === p.id);
    out.push(el("h3", {}, `Cortes históricos en este punto (${evs.length})`));
    if (!evs.length) out.push(el("p", {}, "Sin cortes registrados en la prensa relevada."));
    out.push(...evs.slice().reverse().map((e) => eventoItem(e, false)));
    return out;
  }

  // ------------------------------------------------------------------ Historial
  const filtro = { ruta: "", causa: "", anio: "", punto: "" };
  function selector(key, label, opts) {
    const s = el("select", { id: "f-" + key }, el("option", { value: "" }, "Todos"),
      ...opts.map(([v, t]) => el("option", { value: v }, t)));
    s.value = filtro[key];
    s.addEventListener("change", () => { filtro[key] = s.value; render(); });
    return el("div", {}, el("label", { for: "f-" + key }, label), s);
  }
  function vistaHistorial() {
    const anios = [...new Set(D.eventos.map((e) => e.fecha.slice(0, 4)))].sort().reverse();
    const causas = [...new Set(D.eventos.map((e) => e.causa))].sort();
    const evs = D.eventos.filter((e) => (!filtro.ruta || e.ruta === filtro.ruta) && (!filtro.causa || e.causa === filtro.causa) &&
      (!filtro.anio || e.fecha.startsWith(filtro.anio)) && (!filtro.punto || e.punto_id === filtro.punto));
    const tabla = el("table", { class: "tabla" },
      el("thead", {}, el("tr", {}, el("th", {}, "Año"), el("th", {}, "Con fuente estable"), el("th", {}, "Solo fuentes nuevas"))),
      el("tbody", {}, ...D.por_anio.map((r) => el("tr", {}, el("td", {}, r.anio), el("td", {}, r.estables), el("td", {}, r.solo_nuevas)))));
    return [el("h2", {}, "Historial de cortes"),
      el("div", { class: "filtros" },
        selector("ruta", "Ruta", [["RN9", "RN 9"], ["RN52", "RN 52"]]),
        selector("causa", "Causa", causas.map((c) => [c, CAUSA[c] || c])),
        selector("anio", "Año", anios.map((a) => [a, a])),
        selector("punto", "Punto", D.puntos.map((p) => [p.id, p.nombre]))),
      el("p", {}, el("strong", {}, `${evs.length} de ${D.eventos.length} eventos`)),
      ...evs.slice().reverse().map((e) => eventoItem(e, true)),
      el("h3", {}, "Eventos por año"), tabla,
      el("p", { class: "muted" }, "Fuente estable = medio con archivo desde 2016. Los años recientes tienen más medios: más eventos no significa más cortes.")];
  }

  // ------------------------------------------------------------------ Jama
  function vistaJama() {
    const J = D.jama;
    const out = [el("h2", {}, "Paso de Jama")];
    if (!J.ultimos.length) out.push(el("p", { class: "aviso" }, "No hay capturas del estado del paso en este paquete."));
    if (J.vieja && J.ultimos.length) out.push(el("p", { class: "aviso" }, "Atención: la última captura tiene más de 6 horas al momento de generar el tablero. El estado puede haber cambiado."));
    for (const u of J.ultimos) {
      out.push(el("h3", {}, JAMA[u.fuente] || u.fuente));
      out.push(el("p", {}, el("strong", {}, u.estado), ` · capturado ${u.fetched_at} (hace ${u.horas} h al generar)` + (u.vieja ? " · VIEJO" : "")));
      if (u.error) out.push(el("p", { class: "aviso" }, "Error de la captura: " + u.error));
      if (Object.keys(u.campos).length) out.push(tablaJama(u.campos));
      for (const o of u.otros || []) {
        out.push(el("p", {}, el("strong", {}, o.nombre_paso || "Otro registro")));
        out.push(tablaJama(o));
      }
    }
    out.push(el("h3", {}, "Últimos 7 días"));
    if (!J.linea.length) out.push(el("p", {}, "Sin capturas en los últimos 7 días."));
    out.push(el("ul", { class: "lista" }, ...J.linea.slice().reverse().map((x) =>
      el("li", {}, `${x.fetched_at} · ${JAMA[x.fuente] || x.fuente}: ${x.error ? "error de captura" : x.estado}`))));
    return out;
  }

  // ------------------------------------------------------------------ Limitaciones
  function vistaLimitaciones() {
    const L = D.limitaciones;
    const pct = (a) => (L.eventos ? Math.round((100 * a) / L.eventos) : 0);
    const t = L.dias_evento_prueba;
    const items = [
      `Cobertura de prensa: el catálogo tiene ${L.eventos} eventos; ${L.un_medio} (${pct(L.un_medio)} %) aparecen en un solo medio y ${L.dos_o_mas} en dos o más. Un corte que nadie publicó no está.`,
      `Fuentes estables vs. nuevas: ${L.con_fuente_estable} eventos tienen al menos una fuente con archivo desde 2016; ${L.solo_nuevas} vienen solo de medios más nuevos. Comparar años es engañoso.`,
      `${L.sin_punto} eventos no tienen punto crítico asignado y no entran en la calibración.`,
      `Clima histórico ERA5: grilla de ~28 km; la altura de la celda difiere de la del punto entre ${L.dif_elevacion_min_m ?? "sin dato"} y +${L.dif_elevacion_max_m ?? "sin dato"} m, y ${L.puntos_celda_compartida} puntos comparten celda. Los mm de ERA5 no son la lluvia local.`,
      `Umbrales simples: una regla por causa, igual para todos los puntos. Muestra de prueba chica (días con evento desde ${L.prueba_desde}): aluvión ${t.aluvion}, crecida ${t.crecida}, lluvia ${t.lluvia}, nieve ${t.nieve}.`,
      `El pronóstico (${D.encabezado.pronostico_modelo}) es un modelo distinto de ERA5: se compara en percentiles de su propia climatología, no en mm.`,
      "Una alerta NO significa que la ruta esté cortada ni que se vaya a cortar: indica lluvia o nieve inusual para ese lugar y estación. Consultá siempre a Vialidad Nacional, Gendarmería y el estado oficial del Paso de Jama.",
      "Sin alerta NO significa ruta segura: hay cortes por accidentes, protestas u obras que el clima no predice.",
    ];
    return [el("h2", {}, "Limitaciones"), el("ul", {}, ...items.map((i) => el("li", {}, i)))];
  }

  function vistaUso() {
    const out = [];
    let ul = null;
    for (const b of D.uso) {
      if (b.tipo === "li") { if (!ul) { ul = el("ul", {}); out.push(ul); } ul.append(el("li", {}, b.texto)); continue; }
      ul = null;
      out.push(el(b.tipo === "h1" ? "h2" : b.tipo === "h2" ? "h3" : "p", {}, b.texto));
    }
    return out;
  }

  function pie() {
    const E = D.encabezado;
    const f = document.getElementById("pie");
    f.append(el("p", {}, el("strong", {}, `Datos al ${E.generado} (hora de Jujuy)`),
      E.pronostico_hora ? ` · pronóstico ${E.pronostico_modelo} de las ${E.pronostico_hora}` : " · sin pronóstico"));
    f.append(el("p", {}, `Versión ${E.version} · commit ${E.git_commit} · esquema ${E.schema_version} · paquete ${E.bundle_version}`));
    f.append(el("p", {}, "Medios (enlazados, nunca copiados): ", ...D.fuentes.flatMap((s, i) => [i ? ", " : "", link(s.nombre, s.url)])));
    f.append(el("p", {}, "Licencias: ", ...D.licencias.flatMap((s, i) => [i ? " · " : "", link(s.nombre, s.url)])));
    document.getElementById("sub").textContent = `Datos al ${E.generado}` + (E.pronostico_hora ? ` · pronóstico ${E.pronostico_hora}` : " · sin pronóstico");
  }

  function render() {
    const h = location.hash.replace(/^#/, "") || "mapa";
    const [vistaId, arg] = h.split("/");
    const map = { mapa: vistaMapa, historial: vistaHistorial, jama: vistaJama, limitaciones: vistaLimitaciones, uso: vistaUso };
    const kids = vistaId === "punto" ? vistaPunto(decodeURIComponent(arg || "")) : (map[vistaId] || vistaMapa)();
    vista.replaceChildren(...kids.filter((k) => k));
    for (const a of document.querySelectorAll(".tabs a")) a.classList.toggle("on", a.getAttribute("href") === "#" + (vistaId === "punto" ? "mapa" : vistaId));
  }

  window.addEventListener("hashchange", () => { render(); window.scrollTo(0, 0); });
  pie();
  render();
  if (location.protocol.startsWith("http") && "serviceWorker" in navigator) navigator.serviceWorker.register("sw.js");
})();
