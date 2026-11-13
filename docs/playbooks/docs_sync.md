DOC MAP (what lives where)
Functional (Spanish, for users and jurors):
- README.md — what it does, quick start, limitations, data sources and licenses.
- docs/USO.md — how to read the dashboard: risk levels, what each view means,
  what the alerts do NOT mean. (Created on day 2.)
Technical (English allowed):
- AGENTS.md — rules for agents (mirror of corredor-context).
- docs/FUENTES.md — survey of every candidate news source: status, method, yield.
- docs/SCRAPING.md — how each implemented source is collected.
- docs/DATOS.md — data dictionary for every table and file.
- docs/adr/NNNN-*.md — one ADR per architectural decision.
- CONTRIBUTING.md — workflow, checks, how to add a source.
- CHANGELOG.md — one line per merged PR (Keep a Changelog format).

TRIGGERS (if you change X, update Y in the same PR)
- src/corredor/sources/**      → docs/SCRAPING.md + docs/FUENTES.md
- models.py, storage/**, any table/column → docs/DATOS.md + bump SCHEMA_VERSION + note it in CHANGELOG (Changed)
- a source's parsing logic → bump that class's PARSER_VERSION + CHANGELOG (Fixed/Changed)
- calibration/**, thresholds   → README limitations + docs/USO.md (if it exists)
- CLI commands, Makefile targets, config.yaml keys → README quick start + CONTRIBUTING.md
- dashboard UI                 → docs/USO.md (+ screenshots)
- new dependency, storage or external service → new ADR
- every PR → a line under "## [Unreleased]" in CHANGELOG.md (never edit the version in pyproject.toml in a PR)


RULES
1. Docs describe what the code does NOW, not plans. Plans go in GitHub issues.
2. Never copy pipeline numbers (event counts, thresholds, precision) into docs by hand:
   link to the generated file in reports/ or generate the section from the pipeline.
3. Commands in docs must be copy-paste runnable; run them before committing.
4. Fill the PR template "Docs updated" item with the files touched, or
   "N/A — <reason>". If N/A, add the label no-docs.

PROCEDURE (before opening a PR)
1. git diff --name-only main... and map each path through TRIGGERS.
2. Update the docs; run every command you changed in them.
3. make docs-check must pass.
