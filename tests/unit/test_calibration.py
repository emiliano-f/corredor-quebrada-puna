from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from corredor.calibration.report import section
from corredor.calibration.thresholds import PCT_UNIT, ThresholdCalibrator, season
from corredor.models import ClosureEvent


def features() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    days = pd.date_range("2016-01-01", "2024-12-31", freq="D").date
    frames = []
    for pid, scale in (("a", 1.0), ("b", 3.0)):  # b: same weather, 3x ERA5 bias
        rain = rng.gamma(0.3, 2.0, len(days))
        frames.append(
            pd.DataFrame(
                {
                    "punto_id": pid,
                    "fecha": days,
                    "lluvia_24h_mm": rain * scale,
                    "lluvia_72h_mm": rain * scale * 2,
                    "lluvia_7d_mm": rain * scale * 4,
                    "lluvia_max_horaria_24h_mm": rain * scale / 3,
                    "nieve_24h_cm": 0.0,
                    "nieve_72h_cm": 0.0,
                    "nieve_7d_cm": 0.0,
                }
            )
        )
    df = pd.concat(frames, ignore_index=True)
    for pid, d in EVENTS:
        df.loc[(df.punto_id == pid) & (df.fecha == d), "lluvia_24h_mm"] = 50.0
    return df


EVENTS = [("a", date(2017, 1, 5)), ("b", date(2019, 2, 3)), ("a", date(2024, 1, 20))]


def events() -> list[ClosureEvent]:
    return [
        ClosureEvent(
            evento_id=str(i),
            fecha=d,
            ruta="RN9",
            punto_id=pid,
            causa="aluvion",
            tipo_corte="total",
            fuentes=[f"u{i}"],
            n_medios=1,
            metodo="reglas",
            confianza="alta",
        )
        for i, (pid, d) in enumerate(EVENTS)
    ]


def test_season() -> None:
    assert [season(m) for m in (1, 4, 7, 10, 12)] == ["DJF", "MAM", "JJA", "SON", "DJF"]


def test_percentiles_absorb_cell_bias() -> None:
    df = ThresholdCalibrator().prepare(features().drop(columns=["lluvia_24h_mm"]).assign(
        lluvia_24h_mm=lambda f: np.where(f.punto_id == "b", 3.0, 1.0) * (pd.to_datetime(f.fecha).dt.day_of_year % 7)  # noqa: E501
    ))  # fmt: skip
    a = df[df.punto_id == "a"]["lluvia_24h_mm_pct"].to_numpy()
    b = df[df.punto_id == "b"]["lluvia_24h_mm_pct"].to_numpy()
    assert np.allclose(a, b)


def test_candidates_absolute_and_percentile() -> None:
    results = ThresholdCalibrator().candidates(events(), features())
    assert {r.threshold.causa for r in results} == {"aluvion"}
    pct = [r for r in results if r.threshold.unidad == PCT_UNIT]
    absolute = [r for r in results if r.threshold.unidad == "mm"]
    assert pct
    assert absolute
    p99 = {r.periodo: r for r in pct if r.threshold.variable == "lluvia_24h_mm_pct"
           and r.threshold.umbral == 99.0}  # fmt: skip
    assert p99["train"].aciertos == 2
    assert p99["train"].fallos == 0
    assert p99["test"].aciertos == 1
    assert p99["train"].falsas_alarmas > 0


def test_hit_on_previous_day_and_dry_day_never_alarms() -> None:
    df = pd.DataFrame(
        {"punto_id": "a", "fecha": [date(2016, 1, 1) + timedelta(days=i) for i in range(3000)]}
    )
    for col in ("lluvia_24h_mm", "lluvia_72h_mm", "lluvia_7d_mm", "lluvia_max_horaria_24h_mm"):
        df[col] = 0.0
    df.loc[df.fecha == date(2017, 1, 4), "lluvia_24h_mm"] = 30.0
    ev = events()[:1]
    res = ThresholdCalibrator().candidates(ev, df)
    r = next(
        r for r in res
        if r.threshold.variable == "lluvia_24h_mm_pct" and r.threshold.umbral == 99.0
        and r.periodo == "train"
    )  # fmt: skip
    assert (r.aciertos, r.fallos, r.falsas_alarmas) == (1, 0, 0)


def test_section_renders_both_tables() -> None:
    text = section("Todas", ThresholdCalibrator(), events(), features())
    assert "unidades absolutas" in text
    assert "percentil por celda" in text
    assert "p95" in text


def test_no_events_no_candidates() -> None:
    assert ThresholdCalibrator().candidates([], features()) == []
    assert "Sin candidatos" in section("x", ThresholdCalibrator(), [], features())


def test_merged_variant_pools_rain_causes() -> None:
    from corredor.calibration.thresholds import MERGED

    results = ThresholdCalibrator(groups=MERGED).candidates(events(), features())
    assert {r.threshold.causa for r in results} == {"lluvia"}


def test_section_has_merged_variant_and_counts() -> None:
    text = section("Todas", ThresholdCalibrator(), events(), features())
    assert "Variante: aluvión + crecida = lluvia" in text
    assert "| lluvia |" in text
    assert "(n=" in text
    assert "muestra chica" in text
