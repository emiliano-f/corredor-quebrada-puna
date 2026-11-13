# Test fixtures

Recorded API/feed responses or LISTING pages only, trimmed to the minimum the parser
tests need. Never full article bodies. Tests never touch the network.

- `geo/overpass_*.json`: Overpass answers recorded on 2026-11-13 (maps.mail.ru), trimmed
  to the south end of RN 9, the first ~50 km of RN 52 and the objects the tests use; tags
  reduced. © OpenStreetMap contributors, ODbL.

- `openmeteo/`: Open-Meteo responses recorded on 2026-11-13 for `rn9_volcan`
  (`generationtime_ms` removed). `archive_era5_seamless_trimmed.json` keeps only
  2016-01-01..08 and the final 48 null hours of the 2016→today request.
