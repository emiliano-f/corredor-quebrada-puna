import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from corredor import __version__
from corredor.pipeline import NOT_READY_EXIT, app
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
    assert data["schema_version"] == 1
    assert len(data["sources_hash"]) == 16


@pytest.mark.parametrize("stage", ["datos", "calibrar", "precision", "reporte"])
def test_unwired_stages_fail_clearly(stage: str) -> None:
    result = runner.invoke(app, [stage])
    assert result.exit_code == NOT_READY_EXIT
    assert "todavía no está implementada" in result.output


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
