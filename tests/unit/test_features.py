from datetime import date

import numpy as np
import pandas as pd
import pytest

from corredor.weather.features import FEATURE_COLUMNS, antecedent_features, daily_weather


def hourly(days: int, rain: float = 0.0, start: str = "2024-01-01") -> pd.DataFrame:
    time = pd.date_range(start, periods=days * 24, freq="h")
    return pd.DataFrame(
        {
            "time": time,
            "precipitacion_mm": rain,
            "nieve_cm": 0.0,
            "temp_c": np.tile(np.arange(24, dtype=float), days),
        }
    )


def test_windows_sum_and_need_full_history() -> None:
    df = hourly(8)
    df.loc[df["time"] == pd.Timestamp("2024-01-08 05:00"), "precipitacion_mm"] = 10.0
    df.loc[df["time"] == pd.Timestamp("2024-01-07 23:00"), "precipitacion_mm"] = 4.0
    df.loc[df["time"] == pd.Timestamp("2024-01-01 23:00"), "nieve_cm"] = 3.0
    out = antecedent_features(df).set_index("fecha")
    last = out.loc[date(2024, 1, 8)]
    assert last["lluvia_24h_mm"] == 10.0
    assert last["lluvia_48h_mm"] == 14.0
    assert last["lluvia_72h_mm"] == 14.0
    assert last["lluvia_max_horaria_24h_mm"] == 10.0
    assert last["nieve_7d_cm"] == 0.0
    assert out.loc[date(2024, 1, 7), "nieve_7d_cm"] == 3.0
    assert out.loc[date(2024, 1, 1), "nieve_24h_cm"] == 3.0
    assert out.loc[date(2024, 1, 2), "nieve_24h_cm"] == 0.0
    assert np.isnan(out.loc[date(2024, 1, 1), "lluvia_48h_mm"])
    assert np.isnan(out.loc[date(2024, 1, 6), "lluvia_7d_mm"])
    assert out.loc[date(2024, 1, 7), "lluvia_7d_mm"] == 4.0
    assert list(out.columns) == FEATURE_COLUMNS


def test_missing_hours_are_never_zero() -> None:
    df = hourly(4, rain=1.0)
    df = df[df["time"] != pd.Timestamp("2024-01-03 10:00")]
    out = antecedent_features(df).set_index("fecha")
    assert out.loc[date(2024, 1, 2), "lluvia_24h_mm"] == 24.0
    assert np.isnan(out.loc[date(2024, 1, 3), "lluvia_24h_mm"])
    assert np.isnan(out.loc[date(2024, 1, 4), "lluvia_48h_mm"])
    assert out.loc[date(2024, 1, 4), "lluvia_24h_mm"] == 24.0


def test_nan_values_propagate() -> None:
    df = hourly(2, rain=0.5)
    df.loc[30, "precipitacion_mm"] = np.nan
    out = antecedent_features(df).set_index("fecha")
    assert np.isnan(out.loc[date(2024, 1, 2), "lluvia_24h_mm"])
    assert out.loc[date(2024, 1, 1), "lluvia_24h_mm"] == 12.0


def test_per_point_and_unsorted_duplicates() -> None:
    a = hourly(2, rain=1.0).assign(punto_id="a")
    b = hourly(2, rain=2.0).assign(punto_id="b")
    df = pd.concat([b, a, a.tail(3)]).sample(frac=1.0, random_state=0)
    out = antecedent_features(df)
    assert list(out.columns[:2]) == ["punto_id", "fecha"]
    got = out.set_index(["punto_id", "fecha"])["lluvia_48h_mm"]
    assert got[("a", date(2024, 1, 2))] == 48.0
    assert got[("b", date(2024, 1, 2))] == 96.0


def test_empty_inputs() -> None:
    empty = hourly(0)
    assert antecedent_features(empty).empty
    assert antecedent_features(empty.assign(punto_id="x")).empty
    assert daily_weather(empty, "x") == []
    with pytest.raises(ValueError, match="time"):
        antecedent_features(pd.DataFrame({"x": [1]}))


def test_daily_weather() -> None:
    df = hourly(2, rain=0.25)
    df.loc[df["time"] == pd.Timestamp("2024-01-01 15:00"), "precipitacion_mm"] = 3.0
    df.loc[df["time"] == pd.Timestamp("2024-01-02 15:00"), "temp_c"] = np.nan
    day1, day2 = daily_weather(df, "p")
    assert day1.punto_id == "p"
    assert day1.fecha == date(2024, 1, 1)
    assert day1.precipitacion_mm == pytest.approx(23 * 0.25 + 3.0)
    assert day1.precip_max_horaria_mm == 3.0
    assert (day1.temp_min_c, day1.temp_max_c) == (0.0, 23.0)
    assert day1.nieve_cm == 0.0
    assert day2.temp_max_c is None
    assert day2.temp_min_c is None
    assert day2.precipitacion_mm == 6.0
