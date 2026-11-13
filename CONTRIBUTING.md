# Contributing

Rules for humans and agents live in [AGENTS.md](AGENTS.md). This file covers the workflow.

## Setup and checks

```bash
make setup        # uv sync --frozen + pre-commit install
make check        # lint + typecheck + test + docs-check + audit
make format       # ruff fix + format
make clima        # Open-Meteo archive per point (respects clima.max_llamadas_diarias)
```

`make docs-check` compares your branch against `origin/main`, so run `git fetch origin`
first. `make snapshot-jama` (`uv run corredor snapshot-jama`; Paso de Jama status, see
[docs/SCRAPING.md](docs/SCRAPING.md)) makes one live request per source; in production it
runs only from `.github/workflows/jama_snapshot.yml`. Tests never touch the network: use recorded fixtures under `tests/fixtures/` and
`respx` for HTTP.

## Workflow

- Branch from `main` as `feature/<topic>`; never commit directly to `main`.
- Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`).
- Commit identity: author and committer emails must end in `@users.noreply.github.com`
  (enforced by the `identity-guard` pre-commit hook, `scripts/check_identity.py`).
- Open a PR with the template. CI must be green. Follow
  [docs/playbooks/docs_sync.md](docs/playbooks/docs_sync.md): every PR adds a line under
  `## [Unreleased]` in `CHANGELOG.md`; the `no-docs` label skips the docs guard.
- PRs never change the version in `pyproject.toml`. Bump `SCHEMA_VERSION`
  (`src/corredor/models.py`) on any table/column change and a source's `PARSER_VERSION`
  when its parsing changes.
- `models.py` is frozen after the foundation: add fields only, never change existing
  ones, and say so in the PR.

## Adding a news source

Follow [docs/playbooks/add_news_source.md](docs/playbooks/add_news_source.md). In short:

1. Check robots.txt and record status and date in `docs/FUENTES.md`.
2. If a generic class fits (`wordpress_api`, `sitemap`, `rss`), add an entry under
   `fuentes:` in `config.yaml`; no code needed.
3. Otherwise write `<Outlet>Source(NewsSource)` in `src/corredor/sources/<outlet>.py` on
   top of `PoliteFetcher`, with `PARSER_VERSION = 1`, register it in
   `sources/generic.py::build_sources`, and use `metodo: custom`.
4. Add trimmed fixtures (API/feed responses or listing pages, never article bodies) and
   offline tests; document the source in `docs/SCRAPING.md`.

## Releases

Only the integration session or the owner releases; child sessions never do. `main` is
protected (PR + green CI), so a release is two steps:

1. On an up-to-date, clean `main`: `make release BUMP=patch|minor|major`. It creates
   `release/vX.Y.Z`, bumps `pyproject.toml` with uv (a `.devN` version is finalized
   instead: `0.1.0.dev0` → `0.1.0`), moves the `## [Unreleased]` entries to a dated
   `## [X.Y.Z]` section, commits `chore(release): vX.Y.Z`, pushes and opens a PR. No tag.
2. After that PR is merged: `git switch main && git pull --ff-only && make tag`. It checks
   the version is final (no `.dev`), creates the annotated tag `vX.Y.Z` and pushes only
   the tag. `.github/workflows/release.yml` re-runs the checks, verifies the tag matches
   the `pyproject.toml` version, builds the wheel and publishes a GitHub Release with that
   version's CHANGELOG section.

Pre-1.0 SemVer: MINOR for features, new sources, new tables/columns or breaking schema/CLI
changes; PATCH for fixes and parser repairs.

## Security

Follow the security checklist in AGENTS.md (rule 12) for changes to HTTP fetching,
scraped content, HTML, the LLM extractor, SQL, config, dependencies or workflows. Ruff `S`
rules are on (S101 is ignored in `tests/`); every `noqa: S…` needs a reason. If
`pip-audit` reports a vulnerability with no fix available, ignore only that ID with
`--ignore-vuln <ID>` in the Makefile `audit` target plus a comment and a tracking issue;
never disable the audit job.
