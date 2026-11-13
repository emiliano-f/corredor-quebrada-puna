# ADR 0002 — robots.txt exemption for documented public APIs

- Status: accepted (approved by the owner, Emiliano Flores, on 2026-11-13)
- Date: 2026-11-13

## Context

`PoliteFetcher` checks robots.txt for every URL, APIs included (rule 2 of AGENTS.md). On
2026-11-13 the three Open-Meteo API hosts served `User-agent: *` / `Disallow: /`, so
every weather request raised `DisallowedByRobots`. The documentation site
`open-meteo.com` serves `Allow: /`.

robots.txt is the Robots Exclusion Protocol (RFC 9309) for crawlers. Open-Meteo is not a
site we crawl: it is a documented JSON API, and its published terms
(<https://open-meteo.com/en/terms>) offer the free API for non-commercial use without a
key, under CC BY 4.0, with fixed request limits. The `Disallow: /` keeps crawlers from
indexing API responses; it does not withdraw the API terms.

## Decision

`http.robots_exempt_hosts` in `config.yaml` lists exact hostnames whose robots.txt is not
consulted. Each entry carries `motivo` and `terminos_url`. Scope, exactly these 3 hosts:

| Host | Use | Terms |
|---|---|---|
| `archive-api.open-meteo.com` | Historical Weather API (archive, grid cells, point elevation) | <https://open-meteo.com/en/terms> |
| `api.open-meteo.com` | Forecast API | <https://open-meteo.com/en/terms> |
| `historical-forecast-api.open-meteo.com` | Historical Forecast API (`OpenMeteoClient.historical_forecast`; no downloads yet) | <https://open-meteo.com/en/terms> |

- Exact hostnames only: no wildcards, schemes, ports or paths (validated when the config
  and the fetcher are built). Subdomains and `open-meteo.com` itself are not exempt.
- For exempt hosts `PoliteFetcher` skips **only** the robots.txt check (and the robots
  Crawl-delay, which is never fetched). User-Agent, TLS verification, timeouts, the
  per-host rate limit (>= 2 s), retries with backoff, the 429/5xx no-cache rule and the
  disk cache stay as for any other host.
- Each run logs once which hosts are exempt (`corredor clima` prints it too).

Open-Meteo free-tier limits we respect:

- Fewer than 600 calls/min, 5,000/hour and 10,000/day; non-commercial use; attribution
  under CC BY 4.0 (README "Fuentes de datos y licencias").
- The archive is fetched with ONE request per point for the full range
  (2016-01-01 → today), split by year only if the API rejects it.
- `OpenMeteoClient` counts calls with Open-Meteo's weighting (a request for more than
  14 days or more than 10 variables counts as several calls) in
  `data/clima/llamadas_openmeteo.json` and stops with an error before a request would
  exceed `clima.max_llamadas_diarias` (default 500 per UTC day). At one request per
  host every 2.5 s we stay far below the per-minute and per-hour limits.

## Consequences

- Weather works without keys and stays reproducible from the HTTP and Parquet caches.
- Any new exempt host needs a new line in the table above, the host's usage policy, and
  the owner's approval in the PR. Nominatim/Overpass, if they ever need it, get the same
  treatment (exact hosts and their usage policies here).
- Rule 2 of AGENTS.md states this exception (documented public APIs, host by host, with an
  ADR and the owner's approval).
