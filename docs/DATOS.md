# Data dictionary

Pydantic models in `src/corredor/models.py` define every row. `SCHEMA_VERSION` (currently
**1**) is bumped once per release on any table/column change. Tables live in DuckDB
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

`Threshold` and `ValidationResult` are report rows (calibration), not stored tables yet.

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

| Column | Type | Required | Notes |
|---|---|---|---|
| `evento_id` | str | yes | Stable id. |
| `fecha` | date | yes | |
| `hora` | str | no | |
| `ruta` | `RN9` \| `RN52` \| `otra` | yes | |
| `punto_id` | str | no | `puntos.id`. |
| `km` | float | no | |
| `paraje` | str | no | Place name as reported. |
| `causa` | `aluvion` \| `crecida` \| `nieve` \| `accidente` \| `protesta` \| `obra` \| `otro` | yes | |
| `tipo_corte` | `total` \| `parcial` \| `precaucion` \| `desconocido` | yes | |
| `duracion_horas` | float | no | |
| `fuentes` | list[str] | yes | Article URLs merged into the event. |
| `n_medios` | int | yes | Distinct outlets, excluding sources with `republica: true`. |
| `metodo` | `reglas` \| `llm` | yes | |
| `confianza` | `alta` \| `media` \| `baja` | yes | |
| `notas` | str | no | |

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
| `snapshots/jama_estado.jsonl` (branch `data-snapshots`) | Paso de Jama snapshots, one `jama_estado` row per line. |
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

