# Data dictionary

Pydantic models in `src/corredor/models.py` define every row. `SCHEMA_VERSION` (currently
**3**: `eventos.fecha_inicio`, `eventos.fecha_fin`, `eventos.lado` and `puntos.solo_clima`
added; 2 added `puntos.osm` and `puntos.nota_geo`) is bumped once per release on any
table/column change. Opening an older DuckDB file is safe: before writing, the repository
adds the model columns a table lacks (`ALTER TABLE … ADD COLUMN`, null for old rows). Tables live in DuckDB
(`DuckDBRepository`, `src/corredor/storage/repository.py`) and are exported to Parquet
(one file per table). Only allowlisted tables can be written. Column types come from the
models (`TABLE_MODELS`), not from the first batch; an upsert replaces rows with the same
key inside one transaction, so a failed upsert leaves the table unchanged.

| Table | Model | Key |
|---|---|---|
| `articulos` | `Article` | `source_id`, `url` |
| `eventos` | `ClosureEvent` | `evento_id` |
| `puntos` | `CriticalPoint` | `id` |
| `clima_diario` | `WeatherDay` | `punto_id`, `fecha` |
| `jama_estado` | `JamaEstado` | `fuente`, `fetched_at` |

`Threshold` and `ValidationResult` are report rows (calibration), not stored tables.
`eventos` is derived: `corredor datos` rebuilds it from `articulos` on every run.

## `articulos` — news metadata (never full text)

| Column | Type | Required | Notes |
|---|---|---|---|
| `source_id` | str | yes | `fuentes[].id` in `config.yaml`. |
| `parser_version` | int | yes | `PARSER_VERSION` of the source class that produced the row. |
| `url` | str | yes | Link to the original article. |
| `fecha` | date | yes | Publication date. |
| `fecha_fuente` | `published_time` \| `fallback` | yes | Where `fecha` came from (`fallback` = e.g. sitemap `lastmod`). |
| `titular` | str | yes | Headline. |
| `bajada` | str | no | Short lede only. |
| `fetched_at` | datetime (UTC) | yes | When it was collected. |
| `filtro_slug` | `B` \| `C_solo_ruta` \| null | no | Sitemap slug-filter level that selected it. |

## `eventos` — closure events

Built by `corredor datos` (`catalog.build_events`): `RuleBasedExtractor` reads only the
headline, lede and URL path of each `articulos` row (one event per critical point named in the article), then
`EventDeduplicator` merges mentions of the same closure (see
[SCRAPING.md](SCRAPING.md#event-extraction-and-deduplication)).

| Column | Type | Required | Notes |
|---|---|---|---|
| `evento_id` | str | yes | Stable id: first 16 hex chars of SHA-1 of the event `fecha`, `ruta`, `punto_id` and its sorted article URLs. |
| `fecha` | date | yes | Publication date of the earliest merged article (closures are usually reported the same or next day). |
| `hora` | str | no | |
| `ruta` | `RN9` \| `RN52` \| `otra` | yes | |
| `punto_id` | str | no | `puntos.id`. |
| `km` | float | no | Only when the text says `km N`. |
| `paraje` | str | no | Place name as reported. |
| `causa` | `aluvion` \| `crecida` \| `nieve` \| `accidente` \| `protesta` \| `obra` \| `otro` | yes | |
| `tipo_corte` | `total` \| `parcial` \| `precaucion` \| `desconocido` | yes | |
| `duracion_horas` | float | no | Not extracted yet (always null). |
| `fuentes` | list[str] | yes | Article URLs merged into the event. |
| `n_medios` | int | yes | Distinct outlets, excluding sources with `republica: true`. |
| `metodo` | `reglas` \| `llm` | yes | Today always `reglas` (no LLM provider wired). |
| `confianza` | `alta` \| `media` \| `baja` | yes | `alta`: point and a cause found; `media`: one of them; `baja`: no point and zero or several routes. |
| `notas` | str | no | `viento` for wind without snow (`causa=otro`); a note for administrative/health border closures. |
| `fecha_inicio` | date | no | First article of the merged event (= `fecha`). |
| `fecha_fin` | date | no | Last article merged into the event (follow-ups: reopenings, schedules, "sigue cortada", works after the closure). |
| `lado` | `AR` \| `CL` \| `ambos` \| `desconocido` | no | Only for `rn52_paso_jama`: side of the closure from the text ("lado chileno", Chile, San Pedro de Atacama, Ruta 27/CH-27 → CL; Susques/Argentine side → AR; both → ambos). A Chilean-side closure is a corridor closure (`tipo_corte=total`). |

## `puntos` — critical points

| Column | Type | Required | Notes |
|---|---|---|---|
| `id` | str | yes | |
| `nombre` | str | yes | |
| `ruta` | `RN9` \| `RN52` \| `otra` | yes | |
| `km` | float | no | |
| `lat`, `lon` | float | yes | WGS84, coordinates of the `osm` object (never typed by hand). |
| `verificado` | bool | no | `true` only if `osm` is a node/way within 500 m of the route line. |
| `fuente_geo` | str | no | OSM object and its distance to the route line. |
| `fuente_km` | str | no | How the km was measured (see "Geo data" below). |
| `osm` | str | no | Added by the geo stage: `node/<id>` or `way/<id>` the point comes from. |
| `nota_geo` | str | no | Added by the geo stage: why a point is uncertain or not verified. |
| `solo_clima` | bool | no | Weather-only point (today `ch27_alto`, Ruta CH-27 high section in Chile, OSM node/4375798373, the middle node of way/53264481 'Ruta 27 CH'): has weather, no km, never a risk point on the map. Used for snow events with `lado=CL`. |

`make geo` (`corredor geo`) re-derives `lat`, `lon`, `km`, `verificado`, `fuente_geo` and
`fuente_km` from `osm` and writes `reports/geo_verificacion.md`; it exits with code 1 when
`config.yaml` differs from OSM, so the points are updated by hand from the report.

## `clima_diario` — daily weather per point

| Column | Type | Required | Notes |
|---|---|---|---|
| `punto_id` | str | yes | |
| `fecha` | date | yes | |
| `precipitacion_mm` | float | no | |
| `nieve_cm` | float | no | |
| `temp_max_c`, `temp_min_c` | float | no | |
| `precip_max_horaria_mm` | float | no | |

Source: Open-Meteo Historical Weather API (`OpenMeteoClient.history`, model
`clima.modelo_historico`, default `era5_seamless`), hourly values in local time
(`America/Argentina/Jujuy`, UTC−3) aggregated per calendar day by
`weather.features.daily_weather`: `precipitacion_mm` and `nieve_cm` are daily sums
(mm, cm of fresh snow), `temp_max_c`/`temp_min_c` the hourly 2 m extremes (°C) and
`precip_max_horaria_mm` the wettest hour (mm). A day with any missing hour gets null
values (ERA5 lags about 5 days behind today, so the last days are null until a later
run refreshes them).

## Weather files (`data/clima/`, not tables yet)

| Path | Content |
|---|---|
| `archivo/<model>/<tz>/<lat>_<lon>_<start>_<end>.parquet` | Parquet cache of the archive, keyed by (model, timezone, lat, lon, date range) with 5-decimal coordinates (a cached archive is reused when both coordinates are within 0.000015°, about 1.5 m, so re-rounded coordinates do not trigger a new download); `time`, `precipitacion_mm`, `nieve_cm`, `temp_c`. A later run reuses it and only fetches the last 7 days plus the missing ones. |
| `pronostico/<model>/<tz>/<lat>_<lon>_<from>_<to>.parquet` | Forecast cache (one per hour window): the last 7 days plus the next `hours`. |
| `pronostico_historico/<model>/<tz>/<lat>_<lon>_<start>_<end>.parquet` | Cache of `OpenMeteoClient.historical_forecast` (Historical Forecast API, model passed per call; same key and columns as `archivo/`). Nothing is downloaded yet: day 2 uses it for the forecast model's own climatology (#26). |
| `horario.parquet` | All points, hourly: `punto_id`, `time`, `precipitacion_mm`, `nieve_cm`, `temp_c`. |
| `antecedentes.parquet` | One row per point and day: `punto_id`, `fecha` and the antecedent features below. |
| `grilla.parquet` | One row per point and grid model: `punto_id`, `modelo`, `lat_grilla`, `lon_grilla`, `elev_grilla_m`, `elev_punto_m`, `diferencia_m`, `comparte_celda_con`. |
| `llamadas_openmeteo.json` | Weighted Open-Meteo calls per UTC day (last 7 days) for the daily cap (ADR 0002). |

Antecedent features (`weather.features.antecedent_features`), windows ending at the end
of `fecha` (23:00–24:00 local hour included); a window with any missing hour is NaN,
never zero:

| Column | Unit | Window |
|---|---|---|
| `lluvia_24h_mm`, `lluvia_48h_mm`, `lluvia_72h_mm`, `lluvia_7d_mm` | mm | 24 h, 48 h, 72 h, 7 days (sum) |
| `lluvia_max_horaria_24h_mm`, `lluvia_max_horaria_72h_mm` | mm/h | wettest hour in 24 h / 72 h |
| `nieve_24h_cm`, `nieve_72h_cm`, `nieve_7d_cm` | cm | fresh snowfall sum |

### Model, grid cell and elevation per point

`era5_seamless` combines ERA5 (0.25°, about 28 km) and ERA5-Land (0.1°, about 11 km):
precipitation and snowfall come from ERA5 (ERA5-Land returns no precipitation through
Open-Meteo), 2 m temperature from ERA5-Land, downscaled by Open-Meteo to the point
elevation of its 90 m DEM (Copernicus GLO-90). `OpenMeteoClient.grid_cells` records,
per model in `clima.modelos_grilla`, the cell centre and the cell elevation
(`elevation=nan`, downscaling off) vs that point elevation. The generated table is
`reports/clima_grilla.md`; snapshot of 2026-11-13 for the verified coordinates of
`config.yaml` (Geo, PR #23). Only Lipán bajo (~60 m) and Salinas Grandes (~330 m) moved
enough to change elevations; both stay in the same cells. The other points moved ≤ 1 m
(re-rounding), so their cached archives are reused (cells change if a point moves):

| Point | ERA5 cell (precip., snow) | ERA5 cell elev. − point (m) | ERA5-Land cell (temp.) | ERA5-Land cell elev. − point (m) | Point elev. (m) |
|---|---|---:|---|---:|---:|
| `rn9_volcan` | −24.00, −65.50 (A) | +822 | −23.90, −65.50 (a) | +838 | 2079 |
| `rn9_cuesta_barcena` | −24.00, −65.50 (A) | +917 | −24.00, −65.50 | +704 | 1984 |
| `rn9_tumbaya` | −23.75, −65.50 (B) | +1196 | −23.90, −65.50 (a) | +822 | 2095 |
| `rn9_maimara` | −23.50, −65.50 (C) | +1189 | −23.60, −65.40 (b) | +1025 | 2395 |
| `rn9_tilcara` | −23.50, −65.50 (C) | +1112 | −23.60, −65.40 (b) | +948 | 2472 |
| `rn9_huacalera` | −23.50, −65.25 | +450 | −23.40, −65.40 | +749 | 2656 |
| `rn52_purmamarca_chalala` | −23.75, −65.50 (B) | +863 | −23.70, −65.50 (c) | +738 | 2428 |
| `rn52_lipan_bajo` | −23.75, −65.50 (B) | +698 | −23.70, −65.50 (c) | +573 | 2593 |
| `rn52_abra_potrerillos` | −23.75, −65.75 (D) | −349 | −23.70, −65.70 (d) | −328 | 4204 |
| `rn52_ronqui_angosto` | −23.75, −65.75 (D) | +145 | −23.70, −65.70 (d) | +166 | 3710 |
| `rn52_salinas_grandes` | −23.50, −66.00 | +87 | −23.60, −65.90 | 0 | 3406 |
| `rn52_susques` | −23.50, −66.25 | +30 | −23.40, −66.40 | +249 | 3609 |
| `rn52_paso_jama` | −23.25, −67.00 | +36 | −23.20, −67.10 | −9 | 4281 |

Shared cells (same letter): ERA5 A = Volcán + Cuesta de Bárcena; B = Tumbaya +
Purmamarca/Chalala + Lipán bajo (RN 9 and RN 52 get the same rain); C = Maimará +
Tilcara; D = Abra de Potrerillos + Ronqui Angosto. ERA5-Land a = Volcán + Tumbaya;
b = Maimará + Tilcara; c = Purmamarca/Chalala + Lipán bajo; d = Abra de Potrerillos +
Ronqui Angosto. Points in a shared ERA5 cell have identical precipitation and snowfall
series, so they cannot be told apart by rain.

## `jama_estado` — Paso de Jama status snapshots

| Column | Type | Required | Notes |
|---|---|---|---|
| `fuente` | `mop_cl` \| `argentina_gob_ar` | yes | |
| `fetched_at` | datetime (UTC) | yes | |
| `payload_json` | str | no | JSON array with the Jama record(s), keys sorted, **allowlisted fields only** (`FIELDS` in `src/corredor/sources/jama.py`; anything else, e.g. MOP's `CREATEDBY`/`RESPONSABLE` operator usernames, is never stored). `mop_cl` → ArcGIS attributes of OBJECTID 7: `OBJECTID`, `TRANSITABILIDAD`, `ESTADOTIEMPO`, `ESTADOCALZADA`, `CADENAS`, `RESTRICCIONES`, `HABILITADO`, `ESTADOINFORME`, `FECHA`, `HORA`, `ADESDE`, `AHASTA` (dates/times in epoch ms; the text fields are ArcGIS coded-domain values, no free text). `argentina_gob_ar` → the id 19 record: `id`, `nombre_paso`, `estado_prioridad`, `estado_vialidad`, `fecha_schema`, `fecha_schema_cancilleria`, `fecha_hora_consulta`; plus ids 100/101 only while their status differs from `params.estado_base`. Null when `error` is set. |
| `error` | str | no | Why the snapshot failed (e.g. `HTTP 503`, `FetchError: …`, `DisallowedByRobots: …`, `OBJECTID 7 no está en la respuesta`). |

Source file: `snapshots/jama_estado.jsonl` on the `data-snapshots` branch (never on
`main`), one `JamaEstado` JSON object per line, appended every 3 h by
`.github/workflows/jama_snapshot.yml` (see [SCRAPING.md](SCRAPING.md#paso-de-jama-status-snapshots-srccorredorsourcesjamapy)).
`corredor.sources.jama.read_jsonl(path)` parses it into rows for this table.

## Report rows

- `Threshold`: `causa`, `variable`, `umbral`, `unidad`.
- `ValidationResult`: `threshold`, `periodo` (`train` \| `test`), `aciertos`, `fallos`,
  `falsas_alarmas`.

## Files

| Path | Content |
|---|---|
| `data/` | Gitignored: DuckDB file, Parquet exports, HTTP cache. |
| `data/parquet/<table>.parquet` | One Parquet file per table, written by `corredor datos`. |
| `data/snapshots/jama_estado.jsonl` | Local copy of the `data-snapshots` JSONL that `make datos` loads into `jama_estado`. |
| `reports/calidad_catalogo.md` | `corredor reporte`: articles/events per source, year, route, cause and point; dedup ratio; 1 vs 2+ outlets; local-only events; WordPress-vs-sitemap recall check; share of events from `C_solo_ruta` pages; 20 random events. |
| `reports/revision_manual.csv` | `corredor reporte`: stratified sample, seed 42 — 8 `aluvion`, 8 `crecida`, 8 `nieve`, 6 from the other causes (`estrato` = aluvion/crecida/nieve/otras; fewer if a stratum is smaller) — with headline and URL plus empty `ok_corte` (`si` = closure in the corridor, `no` = not a closure, `fuera` = closure outside the corridor), `ok_fecha`, `ok_punto`, `ok_causa`, `comentario` to fill by hand. Never overwritten once it has labels. The owner's first labels (old random sample) were carried over by URL; the original file is kept as `reports/revision_manual_v1.csv`, and `reports/revision_manual_completar.csv` holds only the rows drawn to complete the strata (counting `ok_corte = si` rows). |
| `reports/control/cortes_conocidos.csv` (+ `.md`) | Owner's hand-built control list (56 known closures, 2016–2026). Read only by `corredor cobertura`; never loaded into DuckDB/Parquet. |
| `reports/control/cobertura.md` | `corredor cobertura`: share of control events matched by the catalog (same route, same point or an event without point, event dates overlapping the control dates ±2 days; E003–E005 count as one), overall, by `confianza_fecha` and by outlet (only outlets we collect vs any other), plus the misses and the matched events. |
| `reports/precision.md` | `corredor precision`: `ok_corte` rate (si / no / fuera), then precision per field (fecha, punto, causa) on the `ok_corte = si` rows only, overall and per `estrato`, each with n = labelled rows. |
| `reports/validacion.md` | `corredor calibrar`: threshold candidates per cause, absolute and per-cell percentile, train 2016–2022 / test 2023→, for all sources and for stable sources only, plus a variant with aluvión + crecida merged as `lluvia`. Each hit/miss/false-alarm value shows n = event-days (point, date) of that period; test cells with n < 10 are marked "muestra chica". Snow at Paso de Jama is also shown by side: `lado=CL` events against `ch27_alto` weather, `AR`/`ambos` against `rn52_paso_jama`, and combined (events with unknown side are counted and left out). |
| `snapshots/jama_estado.jsonl` (branch `data-snapshots`) | Paso de Jama snapshots, one `jama_estado` row per line. |
| `data/checkpoints/<source_id>.json` | Resumable collection state: `units` → `{status: ok\|empty\|missing\|error, updated_at, ...}` per month (sitemaps) or year (WordPress). See SCRAPING.md. |
| `data/recoleccion/<source_id>.json` | Counts of the last `corredor recolectar` run of that source (`CollectionStats.as_dict()`). |
| `data/manifest.json` | Lineage of the last run: `version`, `git_commit`, `schema_version`, `sources_hash` (hash of `fuentes` in `config.yaml`), `generated_at`. |
| `reports/*.md` | Generated reports; each starts with the same lineage header. |
| `reports/geo_verificacion.md` | Critical points: OSM-derived km, distance to the route, verified or not, match with `config.yaml`. |
| `assets/geo/*.geojson` | Committed (needed offline by the dashboard). See "Geo data". |

## Geo data (`assets/geo/`, committed)

Written by `make geo` from OpenStreetMap through Overpass. Every file is a GeoJSON
`FeatureCollection` (WGS84, `[lon, lat]`, 6 decimals) with the foreign members
`attribution: "© OpenStreetMap contributors"`, `license` (ODbL 1.0) and `copyright`
(<https://www.openstreetmap.org/copyright>). Keep them when copying the data: ODbL.

| File | Features | Properties |
|---|---|---|
| `rutas.geojson` | RN 9 and RN 52 (one `LineString` each) | `id`, `nombre`, `longitud_km`, `km_inicio`, `km_fin`, `fuente`, `fuente_km` |
| `ferrocarril.geojson` | Tren Solar line Volcán → Tilcara (`LineString`) | same as above |
| `contexto.geojson` | Tren Solar stations and lithium context points (`Point`) | `tipo` (`estacion_tren_solar` \| `litio`), `nombre`, `osm`, `fuente`, `nota` |
| `puntos.geojson` | Critical points (`Point`), same values as `config.yaml` | `id`, `nombre`, `ruta`, `km`, `verificado`, `osm`, `fuente_geo`, `fuente_km`, `nota_geo` |

How lines and km are built (`src/corredor/geo/routes.py`):

- **RN 9:** OSM ways `highway=*` with `ref=RN9` in the bbox `-24.2,-65.6,-23.15,-65.25`,
  stitched into one polyline (shortest path from the southernmost to the northernmost
  vertex). km = OSM distance along that line + an offset fitted (median) to the OSM
  milestones (`highway=milestone` with `distance`) within 50 m of the line. The milestones
  are all between km 1692 and 1701 (San Salvador de Jujuy); further north the km is
  extrapolated along the OSM geometry and may differ from the official progressive.
- **RN 52:** OSM `relation/1745344`, stitched from the vertex closest to RN 9 (junction near
  Purmamarca, km 0 assumed) to `node/311458189` (Paso de Jama). OSM has no milestones on
  RN 52 and no machine-readable Vialidad Nacional progressive was found, so all RN 52 km
  are OSM distances from the junction.
- **Tren Solar:** OSM `relation/17730839` (`route=train`), stitched from the Volcán stop to
  the Tilcara stop; stations are the relation's named stop/station nodes, ordered along the
  line.
- **Lithium:** `node/13735789123` (Cauchari-Olaroz) and `way/209386890` (Salar de Olaroz,
  centre of the salt flat): the Olaroz operation itself is not mapped in OSM as a named
  object, so its plant location is not shown.

| `reports/clima_grilla.md` | Model, grid cell, cell vs point elevation and shared cells per point (`corredor clima`). |
