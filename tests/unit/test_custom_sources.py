from datetime import UTC, date, datetime
from pathlib import Path

import httpx
import pytest
import respx

from corredor.config import AppConfig, load_config
from corredor.http import FetchResult, PoliteFetcher
from corredor.models import SourceConfig
from corredor.sources.eltribuno import ElTribunoSource, note_key, url_date
from corredor.sources.generic import build_sources
from corredor.sources.vialidadnacional import VialidadNacionalSource, is_jujuy_corridor, short

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures"
NOW = datetime(2026, 11, 13, 21, 0, tzinfo=UTC)
VN = "https://www.argentina.gob.ar/node/96178/noticias"
ET = "https://eltribunodejujuy.com"
EMPTY = "<html><body><p>Sin resultados</p></body></html>"


def html(path: str) -> str:
    return (FIXTURES / path).read_text(encoding="utf-8")


class FakeFetcher:
    """Serves fixtures by URL; unknown URLs are 404. Records every request."""

    def __init__(self, pages: dict[str, str]) -> None:
        self.pages = pages
        self.calls: list[str] = []

    def get(self, url: str, *, refresh: bool = False) -> FetchResult:
        self.calls.append(url)
        body = self.pages.get(url)
        return FetchResult(
            url=url,
            status=200 if body is not None else 404,
            content=(body or "").encode(),
            headers={"content-type": "text/html; charset=utf-8"},
            fetched_at=NOW,
        )


@pytest.fixture
def cfg() -> AppConfig:
    return load_config(ROOT / "config.yaml")


def source_cfg(cfg: AppConfig, source_id: str, **params: object) -> SourceConfig:
    base = next(s for s in cfg.fuentes if s.id == source_id)
    return base.model_copy(update={"params": {**base.params, **params}})


# --- Vialidad Nacional ---------------------------------------------------------------


def test_vialidad_parses_listing_metadata(cfg: AppConfig) -> None:
    src = VialidadNacionalSource(source_cfg(cfg, "vialidadnacional"), FakeFetcher({}))
    items = list(src.parse_listing(html("vialidadnacional/listado_p0.html"), VN, NOW))
    assert len(items) == 16
    first = items[0]
    assert first.url.startswith("https://www.argentina.gob.ar/noticias/")
    assert first.fecha == date(2026, 11, 13)
    assert first.fecha_fuente == "published_time"
    assert first.titular.startswith("El Gobierno Nacional avanza con la etapa IV")
    assert first.bajada.startswith("Mediante el Decreto 1358/2026")
    assert first.parser_version == VialidadNacionalSource.PARSER_VERSION
    assert all(len(a.bajada) <= 300 and len(a.titular) <= 300 for a in items)


def test_vialidad_filters_jujuy_and_stops_on_since(cfg: AppConfig) -> None:
    fetcher = FakeFetcher(
        {
            VN: html("vialidadnacional/listado_p0.html"),
            f"{VN}?page=1": html("vialidadnacional/listado_p1.html"),
        }
    )
    src = VialidadNacionalSource(source_cfg(cfg, "vialidadnacional"), fetcher)
    items = list(src.list_articles(date(2026, 10, 1)))
    assert [a.titular[:45] for a in items] == ["Vialidad Nacional ejecuta trabajos en Jujuy p"]
    # page 1 is entirely older than `since` → no request for page 2
    assert fetcher.calls == [VN, f"{VN}?page=1"]


def test_vialidad_stops_at_last_page_and_max_pages(cfg: AppConfig) -> None:
    pages = {VN: html("vialidadnacional/listado_p0.html"), f"{VN}?page=1": EMPTY}
    fetcher = FakeFetcher(pages)
    src = VialidadNacionalSource(source_cfg(cfg, "vialidadnacional"), fetcher)
    list(src.list_articles(date(2000, 1, 1)))
    assert fetcher.calls == [VN, f"{VN}?page=1"]

    fetcher = FakeFetcher({VN: html("vialidadnacional/listado_p0.html")})
    capped = VialidadNacionalSource(source_cfg(cfg, "vialidadnacional", max_paginas=1), fetcher)
    list(capped.list_articles(date(2000, 1, 1)))
    assert fetcher.calls == [VN]


def test_vialidad_oldest_page_parses(cfg: AppConfig) -> None:
    src = VialidadNacionalSource(source_cfg(cfg, "vialidadnacional"), FakeFetcher({}))
    items = list(src.parse_listing(html("vialidadnacional/listado_p74.html"), VN, NOW))
    assert items
    assert min(a.fecha for a in items) == date(2018, 10, 10)


def test_vialidad_skips_malformed_items(cfg: AppConfig) -> None:
    broken = (
        '<a class="panel" href="/noticias/sin-fecha"><h3>Sin fecha</h3></a>'
        '<a class="panel" href="/noticias/fecha-rota"><time datetime="ayer"></time><h3>X</h3></a>'
        '<a class="panel" href="/otra-cosa"><time datetime="2026-01-01"></time><h3>Y</h3></a>'
        '<a class="panel" href="/noticias/ok"><time datetime="2026-01-02 10:00:00"></time>'
        "<h3>Corte en la Ruta Nacional 52</h3></a>"
    )
    src = VialidadNacionalSource(source_cfg(cfg, "vialidadnacional"), FakeFetcher({}))
    items = list(src.parse_listing(broken, VN, NOW))
    assert [(a.url, a.bajada) for a in items] == [("https://www.argentina.gob.ar/noticias/ok", "")]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Obras en la Ruta Nacional 9 en Jujuy", True),
        ("Corte total en la RN 52 por derrumbe", True),
        ("Trabajos en el Paso de Jama", True),
        ("Repavimentación de la Ruta Nacional 9 en Córdoba", False),
        ("Vialidad recomienda planificar los viajes", False),
    ],
)
def test_is_jujuy_corridor(text: str, expected: bool) -> None:
    assert is_jujuy_corridor(text) is expected


def test_short_never_keeps_long_text() -> None:
    assert short("a  b\n c") == "a b c"
    cut = short("x" * 1000)
    assert len(cut) == 300
    assert cut.endswith("…")


# --- El Tribuno de Jujuy -------------------------------------------------------------


def test_eltribuno_url_helpers() -> None:
    url = f"{ET}/nota/2019-11-27-1-0-0-trabajos-en-la-ruta-52"
    assert url_date(url) == date(2019, 11, 27)
    assert url_date(f"{ET}/nota/2019-13-40-1-0-0-x") is None
    assert url_date(f"{ET}/seccion/informacion-general") is None
    assert note_key(url) == note_key(
        f"{ET}/informacion-general/2019-11-27-1-0-0-trabajos-en-la-ruta-52"
    )


def test_eltribuno_parses_tag_page(cfg: AppConfig) -> None:
    src = ElTribunoSource(source_cfg(cfg, "eltribunojujuy"), FakeFetcher({}))
    items = list(
        src.parse_listing(html("eltribuno/ttag_ruta-52_p1.html"), f"{ET}/ttag/ruta-52", NOW)
    )
    assert len(items) == 12
    first = items[0]
    assert first.url == (
        f"{ET}/informacion-general/2026-8-25-7-20-0-restriccion-en-la-ruta-52-y-mas-de-25-tramos-bajo-precaucion"
    )
    assert first.fecha == date(2026, 8, 25)
    assert first.fecha_fuente == "fallback"
    assert first.titular == "Restricción en la Ruta 52 y más de 25 tramos bajo precaución"


def test_eltribuno_pages_until_repeat_and_dedupes_across_tags(cfg: AppConfig) -> None:
    p1, p3 = html("eltribuno/ttag_ruta-52_p1.html"), html("eltribuno/ttag_ruta-52_p3.html")
    fetcher = FakeFetcher(
        {
            f"{ET}/ttag/ruta-52": p1,
            f"{ET}/ttag/ruta-52/2": p3,
            f"{ET}/ttag/ruta-52/3": p1,  # past the end the site serves page 1 again
            f"{ET}/ttag/paso-de-jama": p3,  # same notes under another tag
        }
    )
    src = ElTribunoSource(
        source_cfg(cfg, "eltribunojujuy", tags=["ruta-52", "paso-de-jama", "no-existe"]), fetcher
    )
    items = list(src.list_articles(date(2000, 1, 1)))
    assert fetcher.calls == [
        f"{ET}/ttag/ruta-52",
        f"{ET}/ttag/ruta-52/2",
        f"{ET}/ttag/ruta-52/3",
        f"{ET}/ttag/paso-de-jama",
        f"{ET}/ttag/paso-de-jama/2",
        f"{ET}/ttag/no-existe",
    ]
    keys = [note_key(a.url) for a in items]
    assert len(keys) == len(set(keys))
    titles = {a.titular for a in items}
    assert "Cuatro derrumbes cortan el paso en la Cuesta de Lipán" in titles
    # tagged ruta-52 but nothing in headline/URL names the corridor
    assert "Vecinos necesitan contar con agua potable y de riego" not in titles
    assert min(a.fecha for a in items).year == 2014


def test_eltribuno_since_filter(cfg: AppConfig) -> None:
    fetcher = FakeFetcher({f"{ET}/ttag/ruta-52": html("eltribuno/ttag_ruta-52_p1.html")})
    src = ElTribunoSource(source_cfg(cfg, "eltribunojujuy", tags=["ruta-52"]), fetcher)
    items = list(src.list_articles(date(2026, 1, 1)))
    assert items
    assert all(a.fecha >= date(2026, 1, 1) for a in items)


def test_eltribuno_skips_malformed_items(cfg: AppConfig) -> None:
    broken = (
        '<article class="nota"><div class="nota__titulo">'
        '<a href="/nota/sin-fecha">X</a></div></article>'
        '<article class="nota"><div class="nota__titulo"><a>sin href</a></div></article>'
        '<article class="nota"></article>'
        '<article class="nota"><div class="nota__titulo">'
        '<a href="/nota/2026-2-3-4-5-6-corte-en-ruta-52"> Corte en ruta 52 </a></div>'
        '<div class="nota__introduccion">Bajada breve</div></article>'
    )
    src = ElTribunoSource(source_cfg(cfg, "eltribunojujuy"), FakeFetcher({}))
    items = list(src.parse_listing(broken, f"{ET}/ttag/x", NOW))
    assert [(a.titular, a.bajada) for a in items] == [("Corte en ruta 52", "Bajada breve")]


# --- registry + real fetcher ---------------------------------------------------------


def test_build_sources_registers_custom_classes(cfg: AppConfig) -> None:
    fetcher = FakeFetcher({})
    by_id = {s.source_id: s for s in build_sources(cfg.fuentes, fetcher)}
    assert isinstance(by_id["vialidadnacional"], VialidadNacionalSource)
    assert isinstance(by_id["eltribunojujuy"], ElTribunoSource)


@respx.mock
def test_vialidad_through_polite_fetcher(cfg: AppConfig, tmp_path: Path) -> None:
    respx.get("https://www.argentina.gob.ar/robots.txt").respond(
        200, text="User-agent: *\nCrawl-delay: 10\nDisallow: /user/\n"
    )
    respx.get(VN).respond(200, html=html("vialidadnacional/listado_p0.html"))
    respx.get(f"{VN}?page=1").respond(200, html=EMPTY)
    sleeps: list[float] = []
    clock = [1000.0]

    def sleep(s: float) -> None:
        sleeps.append(s)
        clock[0] += s

    fetcher = PoliteFetcher(
        "corredor-test/0.1 (+https://example.org)",
        tmp_path / "cache",
        client=httpx.Client(),
        retries=0,
        sleep=sleep,
        clock=lambda: clock[0],
        wall_clock=lambda: NOW.timestamp(),
    )
    src = VialidadNacionalSource(source_cfg(cfg, "vialidadnacional"), fetcher)
    items = list(src.list_articles(date(2026, 1, 1)))
    assert len(items) == 1
    assert sleeps
    assert max(sleeps) >= 10  # Crawl-delay honoured between listing pages


def test_markup_in_headlines_stays_plain_text(cfg: AppConfig) -> None:
    hostile = (
        '<a class="panel" href="/noticias/x"><time datetime="2026-01-02"></time>'
        "<h3>&lt;script&gt;alert(1)&lt;/script&gt; Corte en la RN 52</h3>"
        "<p><img src=x onerror=alert(1)>Bajada</p></a>"
    )
    src = VialidadNacionalSource(source_cfg(cfg, "vialidadnacional"), FakeFetcher({}))
    (item,) = src.parse_listing(hostile, VN, NOW)
    assert item.titular == "<script>alert(1)</script> Corte en la RN 52"  # escaped on render
    assert item.bajada == "Bajada"
