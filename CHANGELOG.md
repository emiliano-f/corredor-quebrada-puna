# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/). Feature PRs add a line under
`## [Unreleased]`; only `make release` turns it into a versioned section.

## [Unreleased]

### Changed
- AGENTS.md rule 2: documented public APIs whose terms allow programmatic use (currently
  Open-Meteo) may skip only the robots.txt check, host by host via `robots_exempt_hosts`,
  with an ADR and the owner's approval.

### Added
- Repository foundation: uv project (Python 3.11), typed models (`SCHEMA_VERSION = 1`),
  `config.yaml` with provisional critical points and the approved source survey,
  `PoliteFetcher` (robots.txt RFC 9309, Crawl-delay, rate limit, retries, disk cache),
  shared extraction regexes, DuckDB repository, lineage manifest and `corredor` CLI.
- Tooling: Makefile, pre-commit (identity guard, ruff, mypy, detect-secrets), docs guard,
  two-step release (`make release` opens a release PR, `make tag` pushes the tag), CI and
  release workflows, Dependabot, PR and issue templates. CodeQL (Python + Actions) runs via
  GitHub default setup.
- Docs: README (es-AR), AGENTS.md, CONTRIBUTING.md, FUENTES.md, SCRAPING.md, DATOS.md,
  ADR 0001 and playbooks.
- Paso de Jama snapshots: `corredor snapshot-jama` (collectors for Vialidad MOP Chile
  ArcGIS and argentina.gob.ar, one request each, failures recorded as `error` lines) and
  the `jama_snapshot.yml` workflow that appends to `snapshots/jama_estado.jsonl` on the
  `data-snapshots` branch every 3 h. `PoliteFetcher.get` gains `refresh=True`.
