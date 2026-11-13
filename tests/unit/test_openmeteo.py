import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

import pandas as pd
import pytest

from corredor.config import ClimaConfig
from corredor.http import FetchResult
from corredor.models import CriticalPoint
from corredor.weather.openmeteo import (
    CallBudgetExceeded,
    CallLedger,
    GridCell,
    OpenMeteoClient,
    OpenMeteoError,
    WeatherClient,
    call_weight,
    parse_hourly,
    shared_cells,
)

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "openmeteo"
NOW = datetime(2026, 11, 13, 18, 30, tzinfo=UTC)  # 15:30 in Jujuy
POINT = CriticalPoint(id="rn9_volcan", nombre="Volcán", ruta="RN9", lat=-23.91709, lon=-65.46402)


def fixture(name: str) -> dict[str, Any]:
    data: dict[str, Any] = json.loads((FIXTURES / name).read_text())
    return data


class FakeFetcher:
    """Answers Open-Meteo URLs from recorded fixtures; records every request."""

    def __init__(self) -> None:
        self.urls: list[str] = []
        self.override: dict[str, tuple[int, bytes]] = {}

    def params(self, i: int = -1) -> dict[str, str]:
        return {k: v[0] for k, v in parse_qs(urlsplit(self.urls[i]).query).items()}

    def get(self, url: str) -> FetchResult:
        self.urls.append(url)
        q = {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}
        status, body = 200, b""
        if "forecast" in url:
            body = json.dumps(fixture("forecast_best_match.json")).encode()
        elif q["start_date"] == q["end_date"]:
            name = (
                f"meta_{q['models']}_nan.json"
                if q.get("elevation") == "nan"
                else "meta_era5_seamless_dem.json"
            )
            body = json.dumps(fixture(name)).encode()
        else:
            data = fixture("archive_era5_seamless_trimmed.json")
            h = data["hourly"]
            lo, hi = q["start_date"], q["end_date"] + "T23:59"
            keep = [i for i, t in enumerate(h["time"]) if lo <= t <= hi]
            data["hourly"] = {k: [v[i] for i in keep] for k, v in h.items()}
            body = json.dumps(data).encode()
        for key, answer in self.override.items():
            if key in url:
                status, body = answer
        return FetchResult(url, status, body, {}, NOW)


@pytest.fixture
def fetcher() -> FakeFetcher:
    return FakeFetcher()


def make(tmp_path: Path, fetcher: FakeFetcher, **cfg: Any) -> OpenMeteoClient:
    return OpenMeteoClient(fetcher, tmp_path, ClimaConfig(**cfg), now=lambda: NOW)


def test_is_a_weather_client(tmp_path: Path, fetcher: FakeFetcher) -> None:
    client: WeatherClient = make(tmp_path, fetcher)
    assert client is not None


def test_history_one_request_full_range_and_parquet_cache(
    tmp_path: Path, fetcher: FakeFetcher
) -> None:
    client = make(tmp_path, fetcher)
    df = client.history(POINT, date(2016, 1, 1), date(2016, 1, 8))
    assert len(fetcher.urls) == 1
    q = fetcher.params()
    assert q["hourly"] == "precipitation,snowfall,temperature_2m"
    assert q["models"] == "era5_seamless"
    assert (q["latitude"], q["longitude"]) == ("-23.91709", "-65.46402")
    assert q["timezone"] == "America/Argentina/Jujuy"
    assert list(df.columns) == ["time", "precipitacion_mm", "nieve_cm", "temp_c"]
    assert len(df) == 8 * 24
    assert df["time"].iloc[0] == pd.Timestamp("2016-01-01 00:00")
    cache = (
        tmp_path
        / "archivo"
        / "era5_seamless"
        / "America_Argentina_Jujuy"
        / "-23.91709_-65.46402_2016-01-01_2016-01-08.parquet"
    )
    assert cache.exists()
    again = client.history(POINT, date(2016, 1, 2), date(2016, 1, 3))
    assert len(fetcher.urls) == 1
    assert len(again) == 48
    assert again["time"].iloc[0] == pd.Timestamp("2016-01-02 00:00")


def test_history_extends_cache_with_tail_only(tmp_path: Path, fetcher: FakeFetcher) -> None:
    client = make(tmp_path, fetcher)
    client.history(POINT, date(2016, 1, 1), date(2016, 1, 3))
    df = client.history(POINT, date(2016, 1, 1), date(2016, 1, 8))
    assert fetcher.params()["start_date"] == "2016-01-01"  # max(start, cached_end - 7 d)
    client.history(POINT, date(2016, 1, 1), date(2016, 1, 20))
    assert fetcher.params()["start_date"] == "2016-01-01"
    assert len(df) == 8 * 24
    assert df["time"].is_unique


def test_history_rejects_inverted_range(tmp_path: Path, fetcher: FakeFetcher) -> None:
    with pytest.raises(ValueError, match="end before start"):
        make(tmp_path, fetcher).history(POINT, date(2016, 1, 2), date(2016, 1, 1))


def test_api_error_is_raised_with_reason(tmp_path: Path, fetcher: FakeFetcher) -> None:
    fetcher.override["v1/archive"] = (400, b'{"error":true,"reason":"Parameter out of range"}')
    with pytest.raises(OpenMeteoError, match="HTTP 400: Parameter out of range"):
        make(tmp_path, fetcher).history(POINT, date(2016, 1, 1), date(2016, 1, 8))
    fetcher.override["v1/archive"] = (200, b"<html>")
    with pytest.raises(OpenMeteoError, match="no es JSON"):
        make(tmp_path, fetcher).history(POINT, date(2016, 1, 1), date(2016, 1, 8))
    fetcher.override["v1/archive"] = (200, b"[]")
    with pytest.raises(OpenMeteoError, match="inesperada"):
        make(tmp_path, fetcher).history(POINT, date(2016, 1, 1), date(2016, 1, 8))
    fetcher.override["v1/archive"] = (200, b'{"hourly": {}}')
    with pytest.raises(OpenMeteoError, match="latitud"):
        make(tmp_path, fetcher).history(POINT, date(2016, 1, 1), date(2016, 1, 8))


def test_parse_hourly_validates() -> None:
    with pytest.raises(OpenMeteoError, match="hourly"):
        parse_hourly({})
    with pytest.raises(OpenMeteoError, match="snowfall"):
        parse_hourly({"hourly": {"time": ["2016-01-01T00:00"], "precipitation": [0.0]}})
    tail = parse_hourly(fixture("archive_era5_seamless_trimmed.json")).tail(48)
    assert tail["precipitacion_mm"].isna().all()


def test_grid_cells_records_model_cell_and_elevations(tmp_path: Path, fetcher: FakeFetcher) -> None:
    cells = make(tmp_path, fetcher).grid_cells(POINT)
    assert [c.modelo for c in cells] == ["era5", "era5_land"]
    era5, land = cells
    assert (era5.lat_grilla, era5.lon_grilla) == (-24.0, -65.5)
    assert era5.elev_punto_m == 2079.0
    assert era5.elev_grilla_m is not None
    assert era5.diferencia_m == era5.elev_grilla_m - 2079.0
    assert land.lat_grilla != era5.lat_grilla or land.lon_grilla != era5.lon_grilla
    assert fetcher.params(1)["elevation"] == "nan"
    assert "elevation" not in fetcher.params(0)


def test_shared_cells() -> None:
    def cell(pid: str, lat: float, model: str = "era5") -> GridCell:
        return GridCell(pid, model, lat, -65.5, 3000.0, None)

    cells = [cell("a", -24.0), cell("b", -24.0), cell("c", -23.5), cell("a", -24.0, "era5_land")]
    assert shared_cells(cells) == {("era5", -24.0, -65.5): ["a", "b"]}
    assert cells[0].diferencia_m is None


def test_forecast_window_and_flag(tmp_path: Path, fetcher: FakeFetcher) -> None:
    client = make(tmp_path, fetcher)
    df = client.forecast(POINT, 48)
    q = fetcher.params()
    assert q["start_hour"] == "2026-11-06T15:00"
    assert q["end_hour"] == "2026-11-15T15:00"
    assert q["models"] == "best_match"
    assert df["pronostico"].any()
    assert not df["pronostico"].all()
    assert not df.loc[df["time"] <= pd.Timestamp("2026-11-13 15:00"), "pronostico"].any()
    client.forecast(POINT, 48)
    assert len(fetcher.urls) == 1
    with pytest.raises(ValueError, match="hours"):
        client.forecast(POINT, 0)


def test_forecast_other_time_zone(tmp_path: Path, fetcher: FakeFetcher) -> None:
    make(tmp_path, fetcher, zona_horaria="UTC").forecast(POINT, 1)
    assert fetcher.params()["start_hour"] == "2026-11-06T18:00"


@pytest.mark.parametrize(
    ("variables", "days", "expected"),
    [(1, 1, 1.0), (3, 14, 1.0), (3, 3970, pytest.approx(85.07, abs=0.01)), (20, 1, 2.0)],
)
def test_call_weight(variables: int, days: float, expected: object) -> None:
    assert call_weight(variables, days) == expected


def test_ledger_stops_before_cap_and_persists(tmp_path: Path) -> None:
    today = [date(2026, 11, 13)]
    path = tmp_path / "ledger.json"
    ledger = CallLedger(path, 10, today=lambda: today[0])
    ledger.reserve(6)
    with pytest.raises(CallBudgetExceeded, match="tope diario de 10"):
        CallLedger(path, 10, today=lambda: today[0]).reserve(5)
    ledger.refund(2)
    assert ledger.used_today() == 4
    today[0] = date(2026, 11, 14)
    ledger.reserve(10)
    assert json.loads(path.read_text()) == {"2026-11-13": 4.0, "2026-11-14": 10.0}


def test_client_counts_weighted_calls_and_refunds_http_cache(tmp_path: Path) -> None:
    class CachedFetcher(FakeFetcher):
        def get(self, url: str) -> FetchResult:
            r = super().get(url)
            return FetchResult(r.url, r.status, r.content, r.headers, r.fetched_at, True)

    client = make(tmp_path, FakeFetcher(), max_llamadas_diarias=3)
    client.grid_cells(POINT)
    assert client.ledger.used_today() == 3
    with pytest.raises(CallBudgetExceeded):
        client.history(POINT, date(2016, 1, 1), date(2016, 1, 8))
    cached = OpenMeteoClient(CachedFetcher(), tmp_path / "b", ClimaConfig(), now=lambda: NOW)
    cached.grid_cells(POINT)
    assert cached.ledger.used_today() == 0


def test_http_cache_hits_bypass_an_exhausted_cap(tmp_path: Path) -> None:
    class PeekFetcher(FakeFetcher):
        def __init__(self) -> None:
            super().__init__()
            self.store: dict[str, FetchResult] = {}

        def cached(self, url: str) -> FetchResult | None:
            return self.store.get(url)

        def get(self, url: str) -> FetchResult:
            r = super().get(url)
            self.store[url] = FetchResult(r.url, r.status, r.content, r.headers, r.fetched_at, True)
            return r

    f = PeekFetcher()
    make(tmp_path, f, max_llamadas_diarias=3).grid_cells(POINT)
    exhausted = make(tmp_path, f, max_llamadas_diarias=3)
    assert exhausted.ledger.used_today() == 3
    assert len(exhausted.grid_cells(POINT)) == 2
    assert len(f.urls) == 3
    assert exhausted.ledger.used_today() == 3


def test_archive_cache_tolerates_rounding_noise_only(tmp_path: Path, fetcher: FakeFetcher) -> None:
    client = make(tmp_path, fetcher)
    client.history(POINT, date(2016, 1, 1), date(2016, 1, 3))
    nudged = POINT.model_copy(update={"lat": POINT.lat - 0.00001, "lon": POINT.lon + 0.00001})
    client.history(nudged, date(2016, 1, 1), date(2016, 1, 3))
    assert len(fetcher.urls) == 1
    moved = POINT.model_copy(update={"lat": POINT.lat + 0.0004})
    client.history(moved, date(2016, 1, 1), date(2016, 1, 3))
    assert len(fetcher.urls) == 2


def test_archive_cache_is_keyed_by_time_zone(tmp_path: Path, fetcher: FakeFetcher) -> None:
    make(tmp_path, fetcher).history(POINT, date(2016, 1, 1), date(2016, 1, 3))
    make(tmp_path, fetcher, zona_horaria="UTC").history(POINT, date(2016, 1, 1), date(2016, 1, 3))
    assert len(fetcher.urls) == 2
    assert fetcher.params()["timezone"] == "UTC"


def test_history_splits_by_year_only_if_rejected(tmp_path: Path) -> None:
    class Rejecting(FakeFetcher):
        def get(self, url: str) -> FetchResult:
            q = {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}
            if q["start_date"][:4] != q["end_date"][:4]:
                self.urls.append(url)
                return FetchResult(url, 400, b'{"error":true,"reason":"range"}', {}, NOW)
            return super().get(url)

    fetcher = Rejecting()
    df = make(tmp_path, fetcher).history(POINT, date(2016, 1, 1), date(2018, 6, 30))
    spans = [(fetcher.params(i)["start_date"], fetcher.params(i)["end_date"]) for i in range(4)]
    assert spans == [
        ("2016-01-01", "2018-06-30"),
        ("2016-01-01", "2016-12-31"),
        ("2017-01-01", "2017-12-31"),
        ("2018-01-01", "2018-06-30"),
    ]
    assert len(df) == 8 * 24
