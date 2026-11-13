1. Check robots.txt and the site's terms; record status and date in docs/FUENTES.md. If disallowed, mark the source Excluded with the reason and stop.
2. Choose the cheapest allowed method, in this order: WordPress REST API (/wp-json/wp/v2/posts) → RSS → sitemap → tag/search/listing pages → custom HTML. If a generic class fits (WordPressApiSource, SitemapSource, RssSource), add the outlet in config.yaml only; otherwise write <Outlet>Source(NewsSource) on top of PoliteFetcher. Set PARSER_VERSION = 1 on a new class; bump it on any later parsing change.
3. Record 2–3 trimmed fixtures (API/feed responses or listing pages, never full article bodies) and write parser tests with no network.
4. Collect with cache under data/, metadata only.
5. Run extraction + dedup and regenerate reports/calidad_catalogo.md; report articles and new events contributed by this source.
6. Follow docs-sync (SCRAPING.md, FUENTES.md, CHANGELOG.md).
7. Open a PR with the template; CI green. If it came from a tier-2 issue, link and close it.
