.PHONY: setup lint format typecheck test docs-check audit check geo snapshot-jama clima datos calibrar precision reporte tablero release tag

UV ?= uv
BUMP ?=

setup:
	$(UV) sync --frozen
	$(UV) run pre-commit install

lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .

format:
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

typecheck:
	$(UV) run mypy

test:
	$(UV) run pytest

docs-check:
	$(UV) run python scripts/check_docs.py

audit:
	$(UV) export --format requirements-txt --no-emit-project --no-hashes --quiet -o .audit-requirements.txt
	$(UV) run pip-audit --disable-pip --no-deps -r .audit-requirements.txt

check: lint typecheck test docs-check audit

geo:
	$(UV) run corredor geo

snapshot-jama:
	$(UV) run corredor snapshot-jama

clima:
	$(UV) run corredor clima

datos:
	$(UV) run corredor manifest
	$(UV) run corredor datos

calibrar:
	$(UV) run corredor calibrar

precision:
	$(UV) run corredor precision

reporte:
	$(UV) run corredor reporte

tablero:
	@echo "El tablero llega el día 2." >&2; exit 2

# Only the integration session or the owner runs these (never child sessions).
# main is protected: `release` opens a release/vX.Y.Z PR; `tag` runs after it is merged.
release:
	@test -n "$(BUMP)" || (echo "Usage: make release BUMP=patch|minor|major" >&2; exit 2)
	$(UV) run python scripts/release.py bump $(BUMP)

tag:
	$(UV) run python scripts/release.py tag
