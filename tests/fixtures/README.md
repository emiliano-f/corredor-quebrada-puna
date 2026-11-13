# Test fixtures

Recorded API/feed responses or LISTING pages only, trimmed to the minimum the parser
tests need. Never full article bodies. Tests never touch the network.

- `geo/overpass_*.json`: Overpass answers recorded on 2026-11-13 (maps.mail.ru), trimmed
  to the south end of RN 9, the first ~50 km of RN 52 and the objects the tests use; tags
  reduced. © OpenStreetMap contributors, ODbL.

- `openmeteo/`: Open-Meteo responses recorded on 2026-11-13 for `rn9_volcan`
  (`generationtime_ms` removed). `archive_era5_seamless_trimmed.json` keeps only
  2016-01-01..08 and the final 48 null hours of the 2016→today request.

## `generic/`

Recorded on 2026-11-13 with the production `PoliteFetcher`, then trimmed:

- `<outlet>_wp_posts.json`: one WP API page (`url`, `headers`, `body`), at most 4 posts,
  `_fields=id,date,link,title,excerpt`, excerpts cut to 400 characters.
- `<outlet>_sitemap.xml[.gz]`: one monthly sitemap cut to 5–6 `<url>` entries.
- `jujuyaldia_sitemap_index.xml`: its Yoast `wp-sitemap.xml` cut to 5 `<sitemap>` children
  (`post-sitemap.xml`, `post-sitemap48–50.xml`, `category-sitemap.xml`);
  `jujuyaldia_sitemap.xml` is `post-sitemap49.xml` cut to 7 `<url>` entries (2016-12 to
  2017-02) without `<image:image>`; `jujuyaldia_pages.json` also names `index_url` and
  `month`.
- `<outlet>_pages.json`: for each selected sitemap URL, a `<head>` rebuilt from that page's
  metadata only (`og:*`, `article:published_time`, minimal JSON-LD). No `<body>`.
- `elsubmarino_feed.xml`: the RSS feed with 4 items, without `content:encoded`, images,
  authors or comments.
- `unsafe_wp_posts.json`: hand-written post with a `<script>` headline (security test).
