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
| `lat`, `lon` | float | yes | WGS84, from OpenStreetMap. |
| `verificado` | bool | no | `false` until checked against OSM. |
| `fuente_geo` | str | no | OSM object used (e.g. `osm:relation/4473252`). |
| `fuente_km` | str | no | Source of the km value. |

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
