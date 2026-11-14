"""End-to-end offline run: articulos in DuckDB → datos → reporte → calibrar → precision."""

from __future__ import annotations

import csv
import json
from datetime import UTC, date, datetime
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import pytest
from typer.testing import CliRunner

from corredor.models import Article
from corredor.pipeline import app
from corredor.storage.repository import DuckDBRepository

ROOT = Path(__file__).resolve().parents[2]
runner = CliRunner()

NEWS = [
    ("todojujuy", "2017-01-05", "Alud en Volcán: cortaron la ruta 9 por completo"),
    ("elsubmarino", "2017-01-06", "Volcán: la ruta 9 sigue cortada por el alud"),
    ("todojujuy", "2024-01-20", "Ruta 52 cortada en Lipán por un aluvión"),
    ("jujuyonline", "2024-01-20", "Lipán: aluvión corta la ruta 52"),
    ("todojujuy", "2019-07-02", "Nevadas en el Abra de Potrerillos: cierran la ruta 52"),
    ("todojujuy", "2020-03-03", "Corte de luz en Tilcara"),
]


def _articles() -> list[Article]:
    return [
        Article(
            source_id=src,
            parser_version=1,
            url=f"https://{src}.test/{i}",
            fecha=date.fromisoformat(d),
            fecha_fuente="published_time",
            titular=title,
            fetched_at=datetime(2026, 11, 13, tzinfo=UTC),
        )
        for i, (src, d, title) in enumerate(NEWS)
    ]


def _weather(path: Path) -> None:
    days = pd.date_range("2016-01-01", "2024-12-31", freq="D").date
    rng = np.random.default_rng(1)
    frames = []
    for pid in ("rn9_volcan", "rn52_lipan_bajo", "rn52_abra_potrerillos"):
        rain = rng.gamma(0.3, 2.0, len(days))
        frame = pd.DataFrame({"punto_id": pid, "fecha": days})
        for col, k in (("lluvia_24h_mm", 1), ("lluvia_72h_mm", 2), ("lluvia_7d_mm", 4),
                       ("lluvia_max_horaria_24h_mm", 0.3)):  # fmt: skip
            frame[col] = rain * k
        for col in ("nieve_24h_cm", "nieve_72h_cm", "nieve_7d_cm"):
            frame[col] = 0.0
        frames.append(frame)
    df = pd.concat(frames, ignore_index=True)
    df.loc[(df.punto_id == "rn9_volcan") & (df.fecha == date(2017, 1, 5)), "lluvia_24h_mm"] = 60
    df.loc[(df.punto_id == "rn52_abra_potrerillos") & (df.fecha == date(2019, 7, 2)),
           "nieve_24h_cm"] = 20  # fmt: skip
    path.parent.mkdir(parents=True)
    df.to_parquet(path)


@pytest.fixture
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    data = tmp_path / "data"
    monkeypatch.setenv("CORREDOR_DATA_DIR", str(data))
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    data.mkdir()
    repo = DuckDBRepository(data / "corredor.duckdb")
    repo.upsert("articulos", _articles())
    repo.close()
    _weather(data / "clima" / "antecedentes.parquet")
    snap = data / "snapshots" / "jama_estado.jsonl"
    snap.parent.mkdir()
    snap.write_text(
        json.dumps(
            {
                "fuente": "mop_cl",
                "fetched_at": "2026-11-13T22:11:07Z",
                "payload_json": "[]",
                "error": None,
            }
        )
        + "\n"
    )
    return tmp_path


def _run(*args: str) -> str:
    result = runner.invoke(app, [*args, "--config", str(ROOT / "config.yaml")])
    assert result.exit_code == 0, result.output
    return result.output


def test_full_offline_pipeline(env: Path) -> None:
    out = _run("datos")
    assert "6 artículos → 5 menciones → 3 eventos" in out
    con = duckdb.connect(str(env / "data" / "corredor.duckdb"), read_only=True)
    rows = con.execute(
        "SELECT punto_id, causa, n_medios, len(fuentes) FROM eventos ORDER BY fecha"
    ).fetchall()
    assert rows == [
        ("rn9_volcan", "aluvion", 2, 2),
        ("rn52_abra_potrerillos", "nieve", 1, 1),
        ("rn52_lipan_bajo", "aluvion", 1, 2),  # jujuyonline republica: not counted
    ]
    assert con.execute("SELECT count(*) FROM puntos").fetchone() == (16,)
    assert con.execute("SELECT count(*) FROM jama_estado").fetchone() == (1,)
    con.close()
    assert (env / "data" / "parquet" / "eventos.parquet").exists()

    _run("reporte")
    quality = (env / "reports" / "calidad_catalogo.md").read_text()
    assert "Eventos (tras dedup): **3**" in quality
    assert "ratio de dedup **1.67**" in quality
    review = list(csv.DictReader((env / "reports" / "revision_manual.csv").open()))
    assert len(review) == 3
    assert review[0]["ok_fecha"] == ""

    _run("calibrar")
    validation = (env / "reports" / "validacion.md").read_text()
    assert "## Todas las fuentes" in validation
    assert "## Solo fuentes estables" in validation
    assert "percentil por celda" in validation

    path = env / "reports" / "revision_manual.csv"
    labelled = [{**r, "ok_fecha": "si", "ok_punto": "no" if i == 0 else "1"}
                for i, r in enumerate(review)]  # fmt: skip
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(review[0]))
        writer.writeheader()
        writer.writerows(labelled)
    _run("precision")
    prec = (env / "reports" / "precision.md").read_text()
    assert "| todos | 100% (n=3) | 67% (n=3) | — (n=0) |" in prec
    assert "| otras | — (n=0) | — (n=0) | — (n=0) |" in prec
    _run("reporte")
    assert "ok_punto" in path.read_text()
    assert next(iter(csv.DictReader(path.open())))["ok_fecha"] == "si"  # labels not overwritten


def test_schema_v1_table_is_migrated(tmp_path: Path) -> None:
    db = tmp_path / "old.duckdb"
    con = duckdb.connect(str(db))
    con.execute("CREATE TABLE puntos (id VARCHAR, nombre VARCHAR)")
    con.execute("INSERT INTO puntos VALUES ('x', 'viejo')")
    con.close()
    repo = DuckDBRepository(db)
    from corredor.config import load_config

    repo.upsert("puntos", load_config(ROOT / "config.yaml").puntos[:1])
    frame = repo.read("puntos")
    repo.close()
    assert {"osm", "nota_geo", "lat"} <= set(frame.columns)
    assert len(frame) == 2
