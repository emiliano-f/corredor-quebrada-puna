from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

from corredor.config import AppConfig, ClimaConfig, Settings, load_config
from corredor.geo.points import CriticalPointRegistry
from corredor.models import SCHEMA_VERSION, ClosureEvent
from corredor.sources.eltribuno import ElTribunoSource
from corredor.sources.generic import (
    SitemapSource,
    UnknownSourceError,
    WordPressApiSource,
    build_sources,
)
from corredor.sources.vialidadnacional import VialidadNacionalSource

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def cfg() -> AppConfig:
    return load_config(ROOT / "config.yaml")


def test_repo_config_loads(cfg: AppConfig) -> None:
    assert 8 <= len(cfg.puntos) <= 14
    assert {p.ruta for p in cfg.puntos} == {"RN9", "RN52"}
    assert len({s.id for s in cfg.fuentes}) == len(cfg.fuentes)


def test_lipan_split_in_two(cfg: AppConfig) -> None:
    ids = {p.id for p in cfg.puntos}
    assert {"rn52_lipan_bajo", "rn52_abra_potrerillos"} <= ids


def test_republisher_flag(cfg: AppConfig) -> None:
    assert [s.id for s in cfg.fuentes if s.republica] == ["jujuyonline"]


def test_sources_hash_is_stable(cfg: AppConfig) -> None:
    assert cfg.sources_hash() == cfg.sources_hash()
    assert len(cfg.sources_hash()) == 16


def test_registry(cfg: AppConfig) -> None:
    reg = CriticalPointRegistry(cfg.puntos)
    assert len(reg) == len(cfg.puntos)
    assert reg.get("rn52_paso_jama").ruta == "RN52"
    assert all(p.ruta == "RN9" for p in reg.by_route("RN9"))


def test_build_sources_uses_generic_classes(cfg: AppConfig) -> None:
    built = build_sources(cfg.fuentes, fetcher=object())  # type: ignore[arg-type]
    kinds = {type(s) for s in built}
    assert kinds == {WordPressApiSource, SitemapSource, VialidadNacionalSource, ElTribunoSource}
    assert all(s.config.tier == 1 for s in built)


def test_build_sources_unknown_custom(cfg: AppConfig) -> None:
    custom = next(s for s in cfg.fuentes if s.metodo == "custom").model_copy(
        update={"enabled": True, "id": "sin-clase"}
    )
    with pytest.raises(UnknownSourceError):
        build_sources([custom], fetcher=object())  # type: ignore[arg-type]


def test_settings_reads_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CORREDOR_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    s = Settings()
    assert s.data_dir == tmp_path
    assert s.llm_api_key is None
    assert s.cache_dir == tmp_path / "cache"
    monkeypatch.setenv("LLM_API_KEY", "x")
    assert Settings().llm_api_key is not None


def test_closure_event_validates_enums() -> None:
    ok = ClosureEvent(
        evento_id="e1",
        fecha=date(2024, 2, 1),
        ruta="RN52",
        causa="aluvion",
        tipo_corte="total",
        fuentes=["https://a"],
        n_medios=1,
        metodo="reglas",
        confianza="alta",
    )
    assert ok.ruta == "RN52"
    with pytest.raises(ValidationError):
        ClosureEvent.model_validate({**ok.model_dump(), "causa": "meteorito"})


def test_schema_version() -> None:
    assert SCHEMA_VERSION == 1


def test_robots_exemptions_are_exactly_open_meteo(cfg: AppConfig) -> None:
    hosts = {e.host for e in cfg.http.robots_exempt_hosts}
    assert hosts == {
        "archive-api.open-meteo.com",
        "api.open-meteo.com",
        "historical-forecast-api.open-meteo.com",
    }
    for e in cfg.http.robots_exempt_hosts:
        assert e.motivo
        assert str(e.terminos_url) == "https://open-meteo.com/en/terms"


def test_robots_exemption_rejects_wildcards_and_duplicates(cfg: AppConfig) -> None:
    raw = cfg.model_dump(mode="json")
    entry = {"motivo": "x", "terminos_url": "https://open-meteo.com/en/terms"}
    raw["http"]["robots_exempt_hosts"] = [{"host": "*.open-meteo.com", **entry}]
    with pytest.raises(ValidationError, match="exact hostname"):
        AppConfig.model_validate(raw)
    raw["http"]["robots_exempt_hosts"] = [{"host": "a.example.org", **entry}] * 2
    with pytest.raises(ValidationError, match="duplicated"):
        AppConfig.model_validate(raw)


def test_clima_config(cfg: AppConfig) -> None:
    assert cfg.clima.desde == date(2016, 1, 1)
    assert cfg.clima.max_llamadas_diarias == 1500
    assert ClimaConfig().max_llamadas_diarias == 500
    assert cfg.clima.modelo_historico == "era5_seamless"
    assert cfg.clima.historical_forecast_url.startswith(
        "https://historical-forecast-api.open-meteo.com/"
    )
