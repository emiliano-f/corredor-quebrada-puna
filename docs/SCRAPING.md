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

## Running a collection

```bash
uv run corredor recolectar                       # every enabled source; sitemaps: sample months only
uv run corredor recolectar --fuente todojujuy    # one source (repeatable)
uv run corredor recolectar --completo            # sitemaps: every month since archivo_desde
```

Articles are upserted into the DuckDB table `articulos` (`data/corredor.duckdb`). Each run
writes the per-source counts (`CollectionStats`) to `data/recoleccion/<source_id>.json`
and resumable checkpoints to `data/checkpoints/<source_id>.json`. `backfill.desde` is the
global start date; a source never goes before its `archivo_desde`. A run stops a source
after `backfill.max_requests_per_run` network requests (cache hits are free); the next run
resumes from the checkpoint.

Checkpoint unit status: `ok` (listed and every selected page fetched), `empty` (the
listing exists and has no entries), `missing` (the listing answered 404), `error`
(network/HTTP error on the listing or on a selected page). `ok`, `empty` and `missing`
are not repeated in later runs; `error` is retried. Each unit also stores `closed`
(the month or year had already ended when it was collected). The current unit is always
re-run, and a unit collected while still open is re-run once more after it ends before
being skipped. Their listings (WP search pages, monthly sitemap) are re-fetched when the
cached copy is older than `min(end of the unit, today)`, so a unit cut by the request cap
resumes from same-day cache instead of starting over; the RSS feed is always refreshed. An empty month and a month with an error are never confused.

Counts in `CollectionStats`: `raw` = entries listed by the outlet (WP: sum of
`X-WP-Total` over every search, with duplicates between terms; sitemap: URLs in the
monthly files; RSS: feed items), `unique` = distinct entries, `selected` = articles kept
after the filter, `by_level` = sitemap `filtro_slug` counts, `pages_missing` = selected
sitemap URLs that answered 404/410 (dropped unless the sitemap carries a headline).

## Implemented sources

All three generic classes live in `src/corredor/sources/generic.py` and are configured
only through `config.yaml` (`metodo` + `params`); there is no per-outlet code.

### `WordPressApiSource` (`metodo: wordpress_api`, `PARSER_VERSION = 1`)

- Endpoint `<base_url>/wp-json/wp/v2/posts` (`params.api_path` overrides it).
- One window per calendar year (`after`/`before`), from `max(backfill.desde,
  archivo_desde)` to today; never deep pagination over the whole archive.
- Searches each term of `patterns.WP_SEARCH_TERMS` (or `params.terms`) with and without
  accents (`patterns.search_variants`), `per_page=100` (`params.per_page`), follows
  `X-WP-TotalPages`, asks only for `_fields=id,date,link,title,excerpt`.
- Results are merged by post id and kept only if `patterns.is_candidate(headline +
  excerpt)` passes. HTML in headline/excerpt is reduced to plain text (entities decoded,
  `<script>`/`<style>` dropped); the excerpt is cut to 300 characters.
- `fecha` = the post `date` (publication date in site time), `fecha_fuente =
  published_time`; `filtro_slug` is empty.
- Checkpoint unit = year.
- Enabled outlets: `elsubmarino`, `radioazultilcara`, `jujuyonline` (`republica: true`,
  does not count as an independent outlet). `jujuyaldia` is not collected this way: its
  robots.txt disallows `/wp-json/`, so it uses `SitemapSource` with `sitemap_indice` (see
  [FUENTES.md](FUENTES.md)).

### `SitemapSource` (`metodo: sitemap`, `PARSER_VERSION = 1`)

- Exactly one of:
  - `params.sitemap_mensual`: one sitemap per month (`{yyyymm}`, `{yyyy}`, `{mm}`
    placeholders);
  - `params.sitemap_indice`: a sitemap index of paginated, date-ordered children (e.g.
    Yoast `post-sitemapN.xml`), kept by the `params.sitemap_hijos` regex (default
    `post-sitemap\d*\.xml$`) and only on the outlet's host. A child's `lastmod` is its
    newest change (an edit to an old post raises it), so it is only an upper bound,
    made monotonic with a suffix minimum: a month skips the children whose bound is
    before it (`index_children_for`), then reads the rest in order and stops at the
    first child listing a post dated after the month. Inside each child only URLs
    published in that month are kept (`/YYYY/MM/` in the path, else
    `news:publication_date`, never `lastmod`; undated URLs are kept). The index is read once per run (refetched if older than a day); an incomplete
    index or a listed child that fails marks the month `error`.
  Plain or gzip (decompression capped at 64 MiB). Parsed with regexes, so no XML entity
  expansion.
- By default only the months in `backfill.muestra_sitemaps`; `--completo` walks every
  month since `archivo_desde`. Months before `archivo_desde` are reported as
  `before_archive` and not requested.
- URLs on another host are skipped. Each URL goes through `patterns.slug_level` (filter C:
  `B` or `C_solo_ruta`); only selected URLs are fetched.
- From each selected page only the `<head>` metadata is read: headline (`og:title` →
  `twitter:title` → JSON-LD `headline` → `<title>`), lede (`og:description` →
  `description`), and date. Date order: `article:published_time` → `itemprop=
  datePublished` → JSON-LD `datePublished` → sitemap `news:publication_date` /
  `lastmod` with `fecha_fuente = fallback`.
- Checkpoint unit = month.
- Enabled outlets: `todojujuy`, `jujuyalmomento`, `somosjujuy`, `prensajujuy` (monthly);
  `jujuyaldia` (index).

### `RssSource` (`metodo: rss`, `PARSER_VERSION = 1`)

- Feed `params.feed_url` (default `<base_url>/feed/`), RSS 2.0 `<item>`s only: a feed has
  no archive, so it is for recent items. `pubDate` (RFC 822) is required; items without a
  parseable date are dropped. Same `patterns.is_candidate` filter as WordPress.
- No outlet uses it yet.

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

### Custom news sources (`metodo: custom`)

One class per outlet, registered by source id in `CUSTOM_CLASSES`
(`src/corredor/sources/generic.py`), so `build_sources` picks them up from `config.yaml`.
Both read only listing pages (never article pages) through `PoliteFetcher`; both sites set
`Crawl-delay: 10`, which the fetcher honours. Headline and lede are whitespace-collapsed and
cut to 300 characters.

| Source (`config.yaml` id) | Class | Requests | Date (`fecha_fuente`) | Kept |
|---|---|---|---|---|
| `vialidadnacional` | `VialidadNacionalSource` (`sources/vialidadnacional.py`) | `GET {base_url}?page=N`, N from 0 (16 items per page, newest first, back to 2018-10). Stops at the first page with no new items, when a whole page is older than `since`, on a non-2xx, or after `params.max_paginas`. | `<time datetime>` of the listing item (`published_time`) | Items whose headline + lede mention Jujuy, a corridor place, or RN 52. RN 9 alone is not enough (it also crosses Córdoba, Santiago del Estero, Tucumán and Salta). |
| `eltribunojujuy` | `ElTribunoSource` (`sources/eltribuno.py`) | `GET {base_url}/ttag/<tag>[/<n>]` for each tag in `params.tags`, up to `params.max_paginas` pages per tag (~12 notes per page). Past the last page the site serves page 1 again, so a page with no new notes ends the tag; a non-2xx (unknown tag) too. | From the URL path `/<seccion>/YYYY-M-D-h-m-s-<slug>` (`fallback`: no `article:published_time` without fetching the note) | Notes whose headline + lede + URL path mention the corridor (`patterns.is_corridor`). The same note appears as `/nota/…` and `/<seccion>/…` and under several tags: deduplicated by the last path segment. |

El Tribuno has no deep archive elsewhere: its sitemaps (`sitemap_lite`, `sitemap-news`,
`sitemap-organico`) list only the latest ~80–200 notes, the RSS page is not a feed,
section listings stop after a few pages and the search (`/busqueda_amp`) returns no
results in the server HTML. Tag pages are the only archive (`/ttag/ruta-52` reaches 2014).

## Adding a source

See [CONTRIBUTING.md](../CONTRIBUTING.md#adding-a-news-source) and
[playbooks/add_news_source.md](playbooks/add_news_source.md). Config-only path for
outlets that fit `wordpress_api`, `sitemap` or `rss`; custom class otherwise.
