# Scraping

How each source is collected. Sources are implemented by the generic-sources and
custom-sources work; until a source is listed under "Implemented sources" it is not
collected. Survey and status of every candidate: [FUENTES.md](FUENTES.md).

## Shared fetcher (`src/corredor/http.py`)

Every production HTTP request goes through `PoliteFetcher.get(url) -> FetchResult`.

| Aspect | Behavior |
|---|---|
| User-Agent | `http.user_agent` in `config.yaml` (project name + repo URL). |
| Rate limit | `max(2.0 s, http.min_interval_s, robots Crawl-delay)` between requests to the same host. |
| robots.txt | Fetched once per host and cached `http.robots_ttl_h` hours. RFC 9309 matcher (`RobotsRules`): group for our product token, else `*`; longest matching rule wins, Allow wins ties; `*` and `$` wildcards. Status codes: 4xx → no restrictions; 5xx or network error → everything disallowed; a body that looks like HTML counts as no rules. Disallowed URLs raise `DisallowedByRobots` (applies to APIs and sitemaps too). Only exception: the exact hosts in `http.robots_exempt_hosts` (the 3 Open-Meteo API hosts, [ADR 0002](adr/0002-api-robots-exemption.md)) skip the robots.txt check; every other rule in this table still applies to them. |
| TLS | Certificate verification always on. |
| Redirects | Followed by hand, at most 5 hops; each hop is checked against robots.txt (`DisallowedByRobots`) and throttled. A redirected robots.txt is followed too (5 hops; more counts as "no rules"). Paths are compared percent-decoded. |
| Retries | 429, 5xx and transport errors: up to `http.retries` retries with exponential backoff, never sooner than `Retry-After`. A `Retry-After` above 600 s fails the request instead of retrying early. |
| Cache | Under `data/cache/` (gitignored), one folder per host, keyed by SHA-256 of the URL. Only 2xx/304 are cached; 404 is cached for 1 hour; 429/5xx are never cached. `get(url, refresh=True)` skips the cache read (live status endpoints) but still writes the cache. |

## OpenStreetMap APIs (geo stage)

`make geo` only talks to OSM services, always through `PoliteFetcher` (same User-Agent,
robots.txt, >= 2 s per host, permanent disk cache: a second run makes no requests).
robots.txt checked on 2026-11-13 (`*` group):

| Host | robots.txt | Use |
|---|---|---|
| `maps.mail.ru` (Overpass mirror) | no rules (redirects to HTML) | primary Overpass endpoint; answers small queries in ~20 s, large ones can return 504 |
| `overpass.kumi.systems`, `overpass.private.coffee` | 404 (no restrictions) | fallbacks, tried in order; both timed out on 2026-11-13 |
| `overpass-api.de` | `Disallow: /api/` | not used |
| `nominatim.openstreetmap.org` | `Disallow: /search`, `/lookup`, `/reverse` | `NominatimGeocoder` raises `DisallowedByRobots`; not used, every point has an OSM id |

Overpass fair use: six small queries per run (two route geometries, milestones, Tren Solar
relation and nodes, objects by id), `timeout:50`. An answer with an error `remark`
raises `OverpassError`; delete `data/cache/<host>/` to refetch. No robots exemption is
used for OSM hosts.

## What is stored

- Stored: URL, outlet (`source_id`), publication date and its provenance
  (`fecha_fuente`), headline, short lede, `parser_version`, `filtro_slug` for sitemaps.
- Never stored in the dataset or committed: full article text. The HTTP cache may hold
  full pages but lives under `data/` and is never published.

## Search and filtering rules (shared by sources)

Implemented in `src/corredor/extraction/patterns.py`:

- WordPress search terms (server-side search ANDs words anywhere in the post, so generic
  words are noise): `patterns.WP_SEARCH_TERMS`. Results are always re-filtered
  client-side on headline + lede with word-boundary, accent-insensitive regexes
  (`alud` never matches `salud`).
- Sitemap slug filter C (`patterns.slug_level`): `B` = corridor place + cause/closure/
  traffic term; `C_solo_ruta` = names RN 9 / RN 52 without a cause term. The full URL
  path is used, trailing slashes and CMS numeric suffixes are removed. Only matching
  slugs are fetched; each article records which level brought it.
- Dates: sitemap `lastmod` is a modification date. Prefer `article:published_time`;
  otherwise mark `fecha_fuente = fallback`.

## Implemented sources

### Paso de Jama status snapshots (`src/corredor/sources/jama.py`)

Not news: live status of the border crossing, stored raw so the history starts accumulating
(neither source keeps an archive). One request per source per run, through
`PoliteFetcher.get(url, refresh=True)` (robots.txt, Crawl-delay and User-Agent as above;
the cache read is skipped because the endpoint is live).

| Source (`config.yaml` id) | `fuente` | Request | Kept |
|---|---|---|---|
| `jama_mop_cl` (`MopChileJama`) | `mop_cl` | `GET {base_url}/query?where=OBJECTID=7&outFields=*&f=json` (ArcGIS MapServer of Vialidad MOP Chile; robots.txt 404 = no restrictions; `params.objectid`) | Allowlisted `attributes` of the OBJECTID 7 feature (status, schedule and timestamp fields; see [DATOS.md](DATOS.md#jama_estado--paso-de-jama-status-snapshots)). Geometry and every other field (including `CREATEDBY`/`RESPONSABLE`, which hold operator usernames) are dropped. |
| `jama_argentina_gob_ar` (`ArgentinaGobArJama`) | `argentina_gob_ar` | `GET {base_url}` (JSON list of every crossing; robots allows it with `Crawl-delay: 10`) | The record(s) in `params.ids` (Jama, id 19), always. The ids in `params.ids_si_cambian` (Jama Norte 100, Jama Sur 101, not open to traffic) only while any field in `params.estado_base` differs from that baseline. Only the allowlisted status/schedule/timestamp fields are kept. The other ~150 crossings are discarded. |

- Field allowlist: each collector keeps only `FIELDS`. Fields outside it are dropped and
  only their NAMES are logged (`INFO corredor.sources.jama: … campos fuera de la allowlist`),
  never their values, so new fields can be reviewed and added on purpose.
- Command: `make snapshot-jama`, i.e. `uv run corredor snapshot-jama [--config config.yaml] [--salida snapshots/jama_estado.jsonl]`
  appends one JSON line per enabled snapshot source (`JamaEstado`, see
  [DATOS.md](DATOS.md#jama_estado--paso-de-jama-status-snapshots)).
- Failures never stop the run: a network error, robots.txt refusal, non-2xx status,
  invalid JSON, an ArcGIS `error` object, a malformed payload or a missing Jama record
  becomes a line with `error` set and `payload_json` empty; the command still exits 0.
- Schedule: [`.github/workflows/jama_snapshot.yml`](../.github/workflows/jama_snapshot.yml),
  `cron: "17 */3 * * *"` (UTC; GitHub may delay scheduled runs by some minutes) plus
  `workflow_dispatch`. It checks out the orphan branch `data-snapshots` (creating it if
  missing), runs the command, commits only `snapshots/jama_estado.jsonl` as
  `github-actions[bot]`, then fetches + rebases (JSONL appends merge with `merge=union`) and
  pushes, retrying once. Concurrency group `jama-snapshot` (`cancel-in-progress: false`);
  `contents: write` only on that job; actions pinned by SHA. Snapshots never land on
  `main`, so they do not trigger CI. GitHub disables scheduled workflows after 60 days
  without repository activity.
- Read the data: `git fetch origin data-snapshots && git show origin/data-snapshots:snapshots/jama_estado.jsonl`.

## Adding a source

See [CONTRIBUTING.md](../CONTRIBUTING.md#adding-a-news-source) and
[playbooks/add_news_source.md](playbooks/add_news_source.md). Config-only path for
outlets that fit `wordpress_api`, `sitemap` or `rss`; custom class otherwise.
