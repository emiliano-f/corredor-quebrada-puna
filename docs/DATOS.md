# Data dictionary

Pydantic models in `src/corredor/models.py` define every row. `SCHEMA_VERSION` (currently
**1**) is bumped once per release on any table/column change. Tables live in DuckDB
(`DuckDBRepository`, `src/corredor/storage/repository.py`) and are exported to Parquet
(one file per table). Only allowlisted tables can be written; upserts replace rows with
the same key.

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
| `payload_json` | str | no | Raw Jama record as returned by the source. |
| `error` | str | no | Set when the request failed. |

## Report rows

- `Threshold`: `causa`, `variable`, `umbral`, `unidad`.
- `ValidationResult`: `threshold`, `periodo` (`train` \| `test`), `aciertos`, `fallos`,
  `falsas_alarmas`.

## Files

| Path | Content |
|---|---|
| `data/` | Gitignored: DuckDB file, Parquet exports, HTTP cache. |
| `data/manifest.json` | Lineage of the last run: `version`, `git_commit`, `schema_version`, `sources_hash` (hash of `fuentes` in `config.yaml`), `generated_at`. |
| `reports/*.md` | Generated reports; each starts with the same lineage header. |
