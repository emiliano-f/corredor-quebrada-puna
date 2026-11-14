import json
from pathlib import Path

import duckdb
import pytest
import respx
import yaml
from typer.testing import CliRunner

from corredor import __version__
from corredor.pipeline import app
from corredor.reports import Lineage, report_header

ROOT = Path(__file__).resolve().parents[2]
runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORREDOR_DATA_DIR", str(tmp_path))
    result = runner.invoke(app, ["manifest", "--config", str(ROOT / "config.yaml")])
    assert result.exit_code == 0, result.output
    data = json.loads((tmp_path / "manifest.json").read_text())
    assert data["version"] == __version__
    assert data["schema_version"] == 3
    assert len(data["sources_hash"]) == 16


def test_report_header() -> None:
    info = Lineage.model_validate(
        {
            "version": "0.1.0",
            "git_commit": "abc123",
            "schema_version": 1,
            "sources_hash": "f" * 16,
            "generated_at": "2026-11-13T00:00:00Z",
        }
    )
    header = report_header("Calidad", info)
    assert header.startswith("# Calidad")
    assert "abc123" in header
    assert "SCHEMA_VERSION 1" in header


def test_clima_stage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from corredor import pipeline

    from .test_openmeteo import FakeFetcher

    class ClosableFetcher(FakeFetcher):
        def close(self) -> None:
            pass

    monkeypatch.setenv("CORREDOR_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pipeline, "build_fetcher", lambda cfg, settings: ClosableFetcher())
    args = ["clima", "--config", str(ROOT / "config.yaml"), "--hasta", "2016-01-08"]
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    assert "Clima: 16/16 puntos, 128 días en clima_diario" in result.output
    report = (tmp_path / "reports" / "clima_grilla.md").read_text()
    assert "rn9_volcan" in report
    assert (tmp_path / "data" / "clima" / "antecedentes.parquet").exists()


def test_build_fetcher_passes_exemptions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from corredor.config import Settings, load_config
    from corredor.pipeline import build_fetcher

    monkeypatch.setenv("CORREDOR_DATA_DIR", str(tmp_path))
    fetcher = build_fetcher(load_config(ROOT / "config.yaml"), Settings())
    assert fetcher.is_robots_exempt("https://archive-api.open-meteo.com/v1/archive")
    assert not fetcher.is_robots_exempt("https://open-meteo.com/")
    fetcher.close()


@respx.mock
def test_recolectar_one_sitemap_source(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    cfg["http"]["min_interval_s"] = 2.0
    cfg["backfill"]["muestra_sitemaps"] = ["2024-02"]
    cfg["fuentes"] = [
        {
            "id": "prueba",
            "nombre": "Prueba",
            "base_url": "https://noticias.example",
            "metodo": "sitemap",
            "tier": 1,
            "enabled": True,
            "params": {"sitemap_mensual": "https://noticias.example/s-{yyyymm}.xml"},
        }
    ]
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("CORREDOR_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr("corredor.http.time.sleep", lambda _s: None)
    respx.get("https://noticias.example/robots.txt").respond(404)
    respx.get("https://noticias.example/s-202402.xml").respond(
        200,
        text="<urlset><url><loc>https://noticias.example/alud-en-volcan-ruta-9-n1</loc>"
        "<lastmod>2024-02-03</lastmod></url></urlset>",
    )
    respx.get("https://noticias.example/alud-en-volcan-ruta-9-n1").respond(
        200, text='<head><meta property="og:title" content="Alud en Volcán"></head>'
    )
    result = runner.invoke(app, ["recolectar", "--config", str(path)])
    assert result.exit_code == 0, result.output
    assert "1 artículos guardados" in result.output
    stats = json.loads((tmp_path / "data" / "recoleccion" / "prueba.json").read_text())
    assert stats["by_level"] == {"B": 1}
    ckpt = json.loads((tmp_path / "data" / "checkpoints" / "prueba.json").read_text())
    assert ckpt["units"]["2024-02"]["status"] == "ok"


def test_recolectar_without_sources(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORREDOR_DATA_DIR", str(tmp_path))
    result = runner.invoke(
        app, ["recolectar", "--config", str(ROOT / "config.yaml"), "--fuente", "nada"]
    )
    assert result.exit_code == 1
    assert "No hay fuentes activas" in result.output


@respx.mock
def test_recolectar_keeps_articles_when_a_source_is_interrupted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    cfg["http"]["min_interval_s"] = 2.0
    cfg["backfill"]["muestra_sitemaps"] = ["2024-01", "2024-02"]
    cfg["fuentes"] = [
        {
            "id": "prueba",
            "nombre": "Prueba",
            "base_url": "https://noticias.example",
            "metodo": "sitemap",
            "tier": 1,
            "enabled": True,
            "params": {"sitemap_mensual": "https://noticias.example/s-{yyyymm}.xml"},
        }
    ]
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")
    monkeypatch.setenv("CORREDOR_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr("corredor.http.time.sleep", lambda _s: None)
    respx.get("https://noticias.example/robots.txt").respond(
        200, text="User-agent: *\nDisallow: /s-202402.xml\n"
    )
    respx.get("https://noticias.example/s-202401.xml").respond(
        200,
        text="<urlset><url><loc>https://noticias.example/alud-en-volcan-ruta-9-n1</loc>"
        "<lastmod>2024-01-03</lastmod></url></urlset>",
    )
    respx.get("https://noticias.example/alud-en-volcan-ruta-9-n1").respond(
        200, text='<head><meta property="og:title" content="Alud en Volcán"></head>'
    )
    result = runner.invoke(app, ["recolectar", "--config", str(path)])
    assert result.exit_code == 1
    assert "1 artículos guardados" in result.output
    assert "fuente interrumpida: DisallowedByRobots" in result.output
    stats = json.loads((tmp_path / "data" / "recoleccion" / "prueba.json").read_text())
    assert stats["errors"][-1].startswith("DisallowedByRobots")
    con = duckdb.connect(str(tmp_path / "data" / "corredor.duckdb"), read_only=True)
    assert con.execute("select count(*) from articulos").fetchone() == (1,)
    con.close()
