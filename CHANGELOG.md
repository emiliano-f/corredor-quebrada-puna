# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/). Feature PRs add a line under
`## [Unreleased]`; only `make release` turns it into a versioned section.

## [Unreleased]

### Changed
- `clima.max_llamadas_diarias` in `config.yaml` 500 → 1500 (owner's decision) to finish
  the 2016→today archive for all 13 points in one day; the code default stays 500.
- Jama snapshots store only allowlisted status/schedule/timestamp fields per source; other
  fields (e.g. MOP `CREATEDBY`/`RESPONSABLE` operator usernames) are dropped and only their
  names are logged. `JamaCollector.PARSER_VERSION` 1 → 2.
- AGENTS.md rule 2: documented public APIs whose terms allow programmatic use (currently
  Open-Meteo) may skip only the robots.txt check, host by host via `robots_exempt_hosts`,
  with an ADR and the owner's approval.
- `jujuyaldia` moved from the WordPress API (its robots.txt disallows `/wp-json/`) to
  `SitemapSource` over its allowed `wp-sitemap.xml` index. 404 cache TTL
  (`http.not_found_ttl_h`) lowered from 24 h to 1 h.
- docs/FUENTES.md: robots.txt column rechecked for all candidates with the production
  parser (all `User-agent: *` groups combined).

### Added
- `OpenMeteoClient.historical_forecast(point, start, end, model)`: hourly series from the
  Historical Forecast API for a given forecast model, cached under
  `data/clima/pronostico_historico/` (no downloads yet; for day 2, #26).
- `SitemapSource` `params.sitemap_indice`/`sitemap_hijos`: paginated sitemap indexes
  (children chosen per month by `lastmod`, URLs filtered by their date).
- Generic sources `WordPressApiSource`, `SitemapSource` and `RssSource` (yearly WP windows,
  monthly sitemaps with slug filter C, resumable checkpoints that tell empty from error,
  per-run request cap), `corredor recolectar` CLI, trimmed fixtures and per-outlet smoke tests.
- Repository foundation: uv project (Python 3.11), typed models (`SCHEMA_VERSION = 1`),
  `config.yaml` with provisional critical points and the approved source survey,
  `PoliteFetcher` (robots.txt RFC 9309, Crawl-delay, rate limit, retries, disk cache),
  shared extraction regexes, DuckDB repository, lineage manifest and `corredor` CLI.
- Tooling: Makefile, pre-commit (identity guard, ruff, mypy, detect-secrets), docs guard,
  two-step release (`make release` opens a release PR, `make tag` pushes the tag), CI and
  release workflows, Dependabot, PR and issue templates. CodeQL (Python + Actions) runs via
  GitHub default setup.
- Geo: `corredor geo` / `make geo` builds RN 9, RN 52 and the Tren Solar line from OSM via
  Overpass (`OverpassClient` with mirror fallback, `OverpassExporter`), writes committed
  GeoJSON with ODbL attribution under `assets/geo/` and `reports/geo_verificacion.md`;
  `CriticalPointRegistry.verify` derives coordinates, km and sources from each point's OSM
  object; `NominatimGeocoder` (robots-bound). `CriticalPoint` gains `osm` and `nota_geo`;
  12 of 13 points verified in `config.yaml`.
- Weather (Child D): `OpenMeteoClient` (archive `era5_seamless` 2016→today in one request
  per point, forecast, grid cell and elevation per point, weighted daily call cap
  `clima.max_llamadas_diarias` = 500, Parquet cache by lat/lon/range), antecedent
  features (24/48/72 h, 7 d, max hourly, snow), `corredor clima` / `make clima` loading
  `clima_diario`, and `reports/clima_grilla.md`.
- `PoliteFetcher`: `http.robots_exempt_hosts` skips only the robots.txt check for the 3
  exact Open-Meteo API hosts (ADR 0002); everything else unchanged.
- Docs: README (es-AR), AGENTS.md, CONTRIBUTING.md, FUENTES.md, SCRAPING.md, DATOS.md,
  ADR 0001 and playbooks.
- Paso de Jama snapshots: `corredor snapshot-jama` (collectors for Vialidad MOP Chile
  ArcGIS and argentina.gob.ar, one request each, failures recorded as `error` lines) and
  the `jama_snapshot.yml` workflow that appends to `snapshots/jama_estado.jsonl` on the
  `data-snapshots` branch every 3 h. `PoliteFetcher.get` gains `refresh=True`.
