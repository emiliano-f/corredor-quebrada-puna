"""OSM export of RN 9, RN 52 and the Volcán–Tilcara railway to GeoJSON (Child C)."""

from __future__ import annotations

from pathlib import Path

from corredor.http import Fetcher


class OverpassExporter:
    def __init__(self, fetcher: Fetcher) -> None:
        self.fetcher = fetcher

    def export(self, out_dir: Path) -> list[Path]:
        raise NotImplementedError("OverpassExporter: pendiente (hija C)")
