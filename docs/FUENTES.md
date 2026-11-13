# FUENTES — relevamiento de fuentes (aprobado 2026-11-13)

Relevamiento hecho con robots.txt, APIs, feeds y sitemaps (más unas pocas páginas de nota para el chequeo de republicación); UA identificable; ≥2,5 s por host; todo cacheado. Los scripts del relevamiento no leían `Crawl-delay` ni verificaban TLS; el fetcher de producción sí lo hace (HANDOFF §7.3).

**Cómo leer los números:** son de un relevamiento rápido. Los estimados WP son cotas superiores (§2) y los conteos de sitemaps usaron una regex con errores conocidos que la subestima (§3). Las dos cosas se corrigen en producción y el número real sale de `reports/calidad_catalogo.md`.

## 1. Listado completo de candidatas

| # | Fuente | URL | robots.txt | Método | Archivo desde | Estado | `republica` | Motivo / nota |
|---|---|---|---|---|---|---|---|---|
| 1 | El Submarino Jujuy | elsubmarinojujuy.com.ar | Permite (solo bloquea Bytespider) | WP REST API | 2013-07 | **Tier 1 genérica** | no | Estable |
| 2 | Jujuy al Día | jujuyaldia.com.ar | Permite; `Content-Signal: ai-train=no, use=reference` | WP REST API | 2010-01 | **Tier 1 genérica** | no | Estable. Solo metadatos (compatible con `use=reference`) |
| 3 | Radio Azul Tilcara | radioazultilcara.com.ar | Permite | WP REST API | 2018-12 | **Tier 1 genérica** | no | Fuente nueva (posterior a 2016) |
| 4 | Jujuy Online | jujuyonline.com | Permite | WP REST API | 2026-04 | **Tier 1 genérica** | **sí** | 29/100 titulares coinciden con Somos Jujuy / Todo Jujuy / Jujuy al Momento; no cuenta en `n_medios` |
| 5 | Todo Jujuy | todojujuy.com | Permite | Sitemap mensual | 2012-01 | **Tier 1 genérica** | no | Estable |
| 6 | Jujuy al Momento | jujuyalmomento.com | Permite | Sitemap mensual | 2011 | **Tier 1 genérica** | no | Estable |
| 7 | Somos Jujuy | somosjujuy.com.ar | Permite | Sitemap mensual (AmuraCMS) | 2018-01 | **Tier 1 genérica** | no | Fuente nueva; falta 2022-09 |
| 8 | Prensa Gobierno de Jujuy | prensa.jujuy.gob.ar | Permite | Sitemap mensual | 2016-05 | **Tier 1 genérica** | no | Fuente nueva (oficial) |
| 9 | El Tribuno de Jujuy | eltribunodejujuy.com | Permite; `Crawl-delay: 10` | RSS + sitemaps recientes; probar listados de sección | — (sin archivo visible) | **Tier 1 custom (Hijo B)** | no | Si no aparece archivo, pasa a Tier 2 |
| 10 | Vialidad Nacional (noticias) | argentina.gob.ar/node/96178/noticias | Permite; `Crawl-delay: 10` | Listado HTML `?page=N`, filtrar Jujuy/RN 9/RN 52 | años (paginado) | **Tier 1 custom (Hijo B)** | no | Feed nacional |
| 11 | Vialidad MOP Chile — ArcGIS Pasos Fronterizos (Jama, OBJECTID 7) | rest-sit.mop.gob.cl/arcgis/rest/services/VIALIDAD/Pasos_Fronterizos/MapServer/0 | 404 (sin restricciones) | Query JSON cada 3 h → tabla `jama_estado` (campos crudos + `fetched_at`) | solo estado actual | **Tier 1 snapshot** | no | Arranca al mergear foundation |
| 12 | Pasos internacionales AR — listado (Jama, id 19) | argentina.gob.ar/seguridad/pasosinternacionales/listado | Permite; `Crawl-delay: 10` | JSON (155 pasos): `estado_prioridad`, `estado_vialidad`, `fecha_schema`, `fecha_hora_consulta` | solo estado actual | **Tier 1 snapshot** | no | Aprobado. 1 request cada 3 h, misma tabla `jama_estado` con columna `fuente`; se guarda solo Jama. Ver §4 |
| 13 | InfoTilcara / Radio RIN | infotilcara.com.ar | Permite | WP REST API | 2023-06 | **Tier 2** | no | 6/507 corredor+causa |
| 14 | El Pregón | pregon.com.ar | Solo Content-Signals, sin Disallow | Sitemap reciente (2,4k) + búsqueda server-side | desconocido | **Tier 2** | — | Profundidad no medida |
| 15 | Que Pasa Jujuy | quepasajujuy.com.ar | `Allow: /` | Búsqueda de CMS propio | desconocido | **Tier 2** | — | Sin sitemap/RSS/WP |
| 16 | Jujuy Dice | jujuydice.com.ar | Permite | Listados por categoría | desconocido | **Tier 2** | — | |
| 17 | UNJu Diario | unjudiario.unju.edu.ar | Permite (bloquea rutas Joomla de admin) | Joomla `/buscar?q=` | desconocido | **Tier 2** | — | RSS vacío; cobertura universitaria |
| 18 | Radio Nacional | radionacional.com.ar | Permite | RSS (WP API da 401) | — | **Tier 2** | — | Nacional |
| 19 | Vía País Jujuy | viapais.com.ar/jujuy | Permite salvo query params | Sitemaps de noticias, RSS | — | **Tier 2** | — | Solo grandes eventos |
| 20 | Infobae | infobae.com | Permite | Sitemaps por categoría | — | **Tier 2** | — | Solo grandes eventos |
| 21 | Calama en Línea (CL) | noticias.calamaenlinea.cl | Permite (salvo wp-admin) | WP REST API | 2020-06 | **Tier 2** | — | Jama: 10/100 corredor+causa (nieve, lado chileno) |
| 22 | Timeline.cl (CL) | timeline.cl | Permite | WP REST API | 2013-07 | **Tier 2** (baja) | — | Jama: 4/100 |
| 23 | pasosfronterizos.gob.cl — noticias (CL) | pasosfronterizos.gob.cl/noticias | 404 (sin restricciones) | Listado HTML (31 páginas) | 2017-03 | **Tier 2** (baja) | — | La búsqueda "jama" no devuelve noticias; el estado diario es una página viva sin archivo |
| 24 | Vialidad Nacional — Estado de rutas | argentina.gob.ar/obras-publicas/vialidad-nacional/estado-de-las-rutas | Permite; `Crawl-delay: 10` | Contenido cargado por JS desde una API con key | solo estado actual | **Tier 2** | — | Investigar si hay endpoint público sin key |
| 25 | GDELT DOC 2.0 | api.gdeltproject.org | n/a | API | 2017-01 (según docs) | **Tier 2 (última prioridad)** | — | 429 desde la VM del relevamiento, **no verificado**: el script cacheaba errores, así que los reintentos pueden no haber salido a la red. Re-probar una vez con el fetcher de producción (1 request cada 5 s) |
| 26 | Radio M Humahuaca | radiomhumahuaca.com.ar | Permite | WP REST API | 2024-04 | **Excluida** | (sí) | Agregador nacional: 98 posts/día de deporte/actualidad nacional, 0/824 corredor+causa |
| 27 | Vialidad Provincial Jujuy | vialidad.jujuy.gob.ar | `Crawl-delay: 30`; bloquea `/wp-*`, `/?s=`, `/*?` | — | noticias hasta 2017 | **Excluida** | — | API bloqueada por robots y archivo desactualizado |
| 28 | Diario Jujuy | diariojujuy.com | — | — | — | **Excluida** | — | Dominio estacionado en venta (HugeDomains) |
| 29 | Jujuy Conecta | diario.jujuyconecta.com | — | — | — | **Excluida** | — | No responde |
| 30 | FM Tributo Tilcara | fmtributotilcara.com | Permite | — | — | **Excluida** | — | Sin noticias |
| 31 | Nueva FM Humahuaca, Radio La Cima Maimará | — | — | — | — | **Excluida** | — | Solo streaming |
| 32 | Radio Municipal Humahuaca | radiomunicipalhumahuaca.net.ar | Permite | WP REST API | 2024 | **Excluida** | — | 7 posts en total |
| 33 | El Mercurio de Calama (CL) | mercuriocalama.cl | `User-agent: * / Disallow: /` | — | — | **Excluida** | — | robots bloquea todo |
| 34 | SoyChile / SoyCalama (CL) | soychile.cl/calama | Permite (salvo /urlJson/) | — | — | **Excluida** | — | Sitemap solo de secciones; buscador sin resultados server-side |
| 35 | SENAPRED (CL) | senapred.cl | Permite | — | — | **Excluida** | — | Sin archivo de alertas viales; el sitemap apunta a `qa2.` |
| 36 | elloa.cl, radiofmcalama.cl, elmercuriodecalama.cl (CL) | — | — | — | — | **Excluida** | — | No resuelven |
| 37 | X / Facebook / Instagram | — | — | — | — | **Excluida** | — | Fuera de alcance |

No hay medio local propio para Volcán, Tumbaya, Purmamarca, Maimará ni Susques: llegan vía las radios de Tilcara y la prensa provincial.

## 2. WordPress: hits crudos vs filtrados

Términos: Lipán, Jama, Volcán, Purmamarca, Susques, Bárcena, Tumbaya, "Salinas Grandes", Maimará, Huacalera, aluvión, alud, derrumbe, desmoronamiento, nevada, crecida.
Filtro sobre título+bajada de los primeros 100 resultados por término: (a) término con borde de palabra (`\balud(es)?\b`, etc.); (b) corredor (`\bruta (nacional )?(n[°º]? ?)?(9|52)\b` o lugar) **y** causa/cierre.

| Fuente | Crudo (suma X-WP-Total) | Muestra | Pasa término \b | Pasa corredor+causa | Estimado filtrado* |
|---|---:|---:|---:|---:|---:|
| El Submarino Jujuy | 23.721 | 1.562 | 323 | 75 | ~330 |
| Jujuy al Día | 44.996 | 1.600 | 343 | 53 | ~480 |
| Radio Azul Tilcara | 1.488 | 881 | 174 | 44 | ~60 |
| Jujuy Online | 1.290 | 714 | 157 | 48 | ~55 |
| InfoTilcara / Radio RIN | 532 | 507 | 135 | 6 | ~6 |
| Radio M Humahuaca | 9.096 | 824 | 65 | 0 | ~0 |
| Calama en Línea (CL) | 3.982 | 511 | 97 | 13 | ~22 |
| Timeline.cl (CL) | 4.233 | 541 | 78 | 5 | ~11 |

\* Proporción de la muestra extrapolada al total crudo, por término; incluye duplicados entre términos. Orden de magnitud, no conteo. **Cota superior:** la muestra son los primeros 100 resultados ordenados por relevancia, que tienen más precisión que la cola.

- `alud` es casi todo ruido: WP matchea "s**alud**" (El Submarino 15.181 crudos → 0 en la muestra; Jujuy al Día 24.886 → 0).
- Los más productivos: aluvión, desmoronamiento, crecida, nevada, Jama.

## 3. Sitemaps: páginas a bajar 2016-01 → 2026-11

Candidato = slug con lugar/ruta del corredor **y** término de causa/cierre.
- **A (anterior):** causas = alud, aluvión, derrumbe, desmoronamiento, deslave, nevada/nieve, crecida, corte/cortada, interrumpido, intransitable, cerrado/cierre, desvío, inhabilitado, socavón, anegamiento.
- **B (ampliado):** A + transitabilidad, tránsito, `km N`/`kilómetro N`. Las variantes de ruta (`ruta-9`, `ruta-52`, `ruta-nacional-9`, `rn-9`, `rn-52`) ya estaban en el lado "corredor", y corte, cortada e intransitable ya estaban en A.
- **C (cota alta):** B + cualquier slug que nombre RN 9 / RN 52 aunque no tenga término de causa.

| Fuente | URLs | A | **B** | C | 2017-01 (A/B/C) | 2024-02 (A/B/C) | 2026-08 (A/B/C) |
|---|---:|---:|---:|---:|---|---|---|
| Todo Jujuy | 165.237 | 274 | **335** | 662 | 18/18/38 | 1/1/3 | 15/18/30 |
| Jujuy al Momento | 164.382 | 235 | **263** | 580 | 15/17/28 | 2/2/5 | 2/2/10 |
| Somos Jujuy | 126.538 | 219 | **257** | 585 | sin archivo | 0/0/5 | 11/12/14 |
| Prensa Gob. Jujuy | 42.391 | 28 | **37** | 70 | 4/5/11 | 0/0/1 | 3/3/4 |
| **Total** | 498.548 | 756 | **892** | 1.897 | | | |

- B ≈ 892 páginas ≈ 37 min a 2,5 s/página. C ≈ 1.900 páginas ≈ 80 min.
- **Elegido: C.** Cada artículo registra `filtro_slug` (B | C_solo_ruta); el reporte de calidad mide cuántos eventos aportan solo las páginas C_solo_ruta. Si son menos del 5 %, se propone volver a B.
- El filtro por slug pierde notas con slug genérico; el chequeo de recall (§5) lo mide.
- **Los conteos A/B/C subestiman.** La regex del relevamiento no reconocía "Nº"/"nro"/"número" en la ruta, formas como "cierran"/"cortaron", ni causas como viento blanco o temporal, y descartaba las URLs con barra final. La versión corregida (HANDOFF §7.1–7.2) va a dar más candidatos; recalcular el estimado al implementar `SitemapSource`.
- Los meses vacíos (Somos Jujuy 2022-09, Prensa 2016-01→04) pueden ser errores de red cacheados como vacío: re-verificar.
- `lastmod` no es la fecha de publicación: se usa `article:published_time` y se marca el fallback.

## 4. Paso de Jama — snapshots de estado

- **Chile (Tier 1):** ArcGIS MOP, `.../MapServer/0/query?where=OBJECTID=7&outFields=*&f=json`. Campos: `TRANSITABILIDAD`, `ESTADOTIEMPO`, `CADENAS`, `RESTRICCIONES`, `HABILITADO`, `FECHA`, `HORA`, `ADESDE`, `AHASTA`, etc. Una consulta cada 3 h; se guarda el JSON crudo + `fetched_at` en `jama_estado`.
- **Argentina (Tier 1, aprobado):** `GET /seguridad/pasosinternacionales/listado` devuelve un JSON con los 155 pasos; Jama es `id: 19` (también vienen Jama Norte 100 y Jama Sur 101, no habilitados). Campos: `estado_prioridad` (ABIERTO/CERRADO), `estado_vialidad` (HABILITADA/…), `fecha_schema`, `fecha_schema_cancilleria`, `fecha_hora_consulta`, lat/lon. robots lo permite, con `Crawl-delay: 10`. Una sola request cada 3 h está muy por debajo del límite. La página de detalle (`/detalle/ruta/19/Jama`) solo agrega el clima del SMN y las horas de actualización de Gendarmería y Vialidad: no hace falta scrapearla.
- **Ejecución:** workflow programado de GitHub Actions cada 3 h → `snapshots/jama_estado.jsonl` en la rama `data-snapshots` (no en `main`). Detalle en HANDOFF §3.6, punto 26.
- Sin historial en ninguna de las dos: el valor empieza a acumularse desde que corre el colector, y sirve para verificar pronósticos y alertas en vivo, no para calibrar el pasado.

## 5. Chequeo de recall (va en `reports/calidad_catalogo.md`)

Eventos encontrados en medios WP (búsqueda por API, sin filtro de slug) que no tienen ningún evento en los medios de sitemap en la misma fecha ±2 días y en el mismo tramo/ruta. Se reporta por año y por medio de sitemap, solo en el período en que ambos tienen archivo.

## 6. `archivo_desde`

Estables (≤2016-01-01): Jujuy al Día 2010-01, Jujuy al Momento 2011, Todo Jujuy 2012-01, El Submarino 2013-07.
Nuevas: Prensa Jujuy 2016-05, Somos Jujuy 2018-01, Radio Azul 2018-12, Jujuy Online 2026-04 (republica). Snapshots de Jama: desde la fecha en que arranca el colector.
