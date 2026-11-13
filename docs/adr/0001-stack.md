# ADR 0001 — Stack

- Status: accepted
- Date: 2026-11-13

## Context

A solo project with a fixed demo date that must run offline on a phone, be reproducible
from a clean clone and respect the news outlets it reads.

## Decisions

- **DuckDB + Parquet.** Embedded, no server, fast analytical SQL over a few hundred
  thousand rows; Parquet exports are portable and easy to ship with an offline
  dashboard. Values are always bound as parameters (registered DataFrames), and table
  names come from an allowlist.
- **Open-Meteo.** Free, no API key, archive (ERA5-based) back to 2016 plus forecast with
  the same variables, CC BY 4.0. Limitation: grid-cell elevation can differ from the real
  point, especially in the Puna.
- **Rules-first extraction.** Regexes are deterministic, cheap, testable and run without
  any key. An optional LLM extractor only runs with `LLM_API_KEY`, is cached, treats
  article text as untrusted data and its output is validated against `ClosureEvent`.
- **Config-driven generic sources.** Most outlets expose a WordPress API, RSS or monthly
  sitemaps, so one class per method plus a `config.yaml` entry covers them; custom
  classes only for outlets that need HTML parsing. One `PoliteFetcher` centralizes
  robots.txt, rate limits, retries and caching.
- **uv + Python 3.11**, ruff, strict mypy, pytest with recorded fixtures, pre-commit and
  GitHub Actions.

## Consequences

Adding an outlet is usually a config change. Thresholds are simple and global, which is
explainable but not a hydrological model. Coverage depends on press coverage.
