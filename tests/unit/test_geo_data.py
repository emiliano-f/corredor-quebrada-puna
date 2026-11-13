"""Committed geo data (config.yaml points + assets/geo) stays consistent and attributed."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from corredor.config import load_config
from corredor.pipeline import app

ROOT = Path(__file__).resolve().parents[2]
GEO = ROOT / "assets" / "geo"


def test_config_points_verified_with_sources() -> None:
    points = load_config(ROOT / "config.yaml").puntos
    verified = [p for p in points if p.verificado]
    assert 8 <= len(verified) <= 12
    for p in points:
        assert p.osm
        assert p.fuente_geo.startswith(f"OSM {p.osm}")
        assert p.fuente_km
        assert p.km
        if not p.verificado:
            assert p.nota_geo, f"{p.id}: an unverified point must say why"
    for ruta in ("RN9", "RN52"):
        kms = [p.km for p in points if p.ruta == ruta]
        assert kms == sorted(kms), f"{ruta} points must be listed in road order"


def test_lipan_split_in_two_points() -> None:
    ids = {p.id: p for p in load_config(ROOT / "config.yaml").puntos}
    bajo, cumbre = ids["rn52_lipan_bajo"], ids["rn52_abra_potrerillos"]
    assert bajo.km is not None
    assert cumbre.km is not None
    assert bajo.km < cumbre.km


@pytest.mark.parametrize(
    "name", ["rutas.geojson", "ferrocarril.geojson", "contexto.geojson", "puntos.geojson"]
)
def test_committed_geojson_has_osm_attribution(name: str) -> None:
    data = json.loads((GEO / name).read_text(encoding="utf-8"))
    assert data["type"] == "FeatureCollection"
    assert data["features"]
    assert data["attribution"] == "© OpenStreetMap contributors"
    assert "ODbL" in data["license"]


def test_committed_points_geojson_matches_config() -> None:
    points = {p.id: p for p in load_config(ROOT / "config.yaml").puntos}
    feats = json.loads((GEO / "puntos.geojson").read_text(encoding="utf-8"))["features"]
    assert {f["properties"]["id"] for f in feats} == set(points)
    for f in feats:
        p = points[f["properties"]["id"]]
        assert f["geometry"]["coordinates"] == [p.lon, p.lat]
        assert f["properties"]["verificado"] == p.verificado
        assert f["properties"]["km"] == p.km


def test_cli_geo_writes_geojson_and_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import corredor.pipeline as pipeline
    from tests.unit.test_geo import FixtureFetcher

    class Fake(FixtureFetcher):
        def __init__(self, *args: object, **kwargs: object) -> None:
            super().__init__()

        def close(self) -> None:
            pass

    monkeypatch.setattr(pipeline, "PoliteFetcher", Fake)
    monkeypatch.setenv("CORREDOR_DATA_DIR", str(tmp_path / "data"))
    report = tmp_path / "geo.md"
    result = CliRunner().invoke(
        app,
        ["geo", "--config", str(ROOT / "config.yaml"), "--salida", str(tmp_path / "geo"),
         "--informe", str(report)],
    )  # fmt: skip
    # The fixtures are trimmed, so far points differ from config.yaml: exit 1 + report.
    assert result.exit_code == 1, result.output
    assert (tmp_path / "geo" / "rutas.geojson").exists()
    text = report.read_text(encoding="utf-8")
    assert text.startswith("# Verificación de puntos críticos")
    assert "OpenStreetMap" in text
