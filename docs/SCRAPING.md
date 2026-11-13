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
| robots.txt | Fetched once per host and cached `http.robots_ttl_h` hours. RFC 9309 matcher (`RobotsRules`): group for our product token, else `*`; longest matching rule wins, Allow wins ties; `*` and `$` wildcards. Status codes: 4xx → no restrictions; 5xx or network error → everything disallowed; a body that looks like HTML counts as no rules. Disallowed URLs raise `DisallowedByRobots` (applies to APIs and sitemaps too). |
| TLS | Certificate verification always on. |
| Redirects | Followed by hand, at most 5 hops; each hop is checked against robots.txt (`DisallowedByRobots`) and throttled. A redirected robots.txt is followed too (5 hops; more counts as "no rules"). Paths are compared percent-decoded. |
| Retries | 429, 5xx and transport errors: up to `http.retries` retries with exponential backoff, never sooner than `Retry-After`. A `Retry-After` above 600 s fails the request instead of retrying early. |
| Cache | Under `data/cache/` (gitignored), one folder per host, keyed by SHA-256 of the URL. Only 2xx/304 are cached; 404 is cached for 1 hour; 429/5xx are never cached. |

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

None yet.

## Adding a source

See [CONTRIBUTING.md](../CONTRIBUTING.md#adding-a-news-source) and
[playbooks/add_news_source.md](playbooks/add_news_source.md). Config-only path for
outlets that fit `wordpress_api`, `sitemap` or `rss`; custom class otherwise.
