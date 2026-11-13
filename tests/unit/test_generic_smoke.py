"""One offline smoke test per configured generic outlet, on recorded and trimmed responses
(tests/fixtures/generic: WP API pages, monthly sitemaps or a sitemap index with one child,
and article <head> metadata)."""

import json
import re
from collections.abc import Callable
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest
import respx

from corredor.config import load_config
from corredor.http import PoliteFetcher
from corredor.models import SourceConfig
from corredor.sources.generic import GenericOptions, SitemapSource, WordPressApiSource

from .conftest import FIXTURES

ROOT = Path(__file__).resolve().parents[2]
GENERIC = FIXTURES / "generic"
GENERIC_METHODS = {"wordpress_api", "sitemap", "rss"}
# Expected yield of each recorded fixture: WP = candidates; sitemap = filtro_slug levels.
EXPECTED_WP = {"elsubmarino": 2, "radioazultilcara": 1, "jujuyonline": 2}
EXPECTED_SITEMAP = {
    "todojujuy": {"B": 2, "C_solo_ruta": 1},
    "jujuyalmomento": {"B": 2, "C_solo_ruta": 1},
    "somosjujuy": {"B": 2, "C_solo_ruta": 1},
    "prensajujuy": {"B": 2},
    "jujuyaldia": {"B": 2, "C_solo_ruta": 1},
}


def enabled_generic() -> list[SourceConfig]:
    cfg = load_config(ROOT / "config.yaml")
    return [s for s in cfg.fuentes if s.enabled and s.metodo in GENERIC_METHODS]


def test_every_enabled_generic_outlet_has_a_smoke_fixture() -> None:
    ids = {s.id for s in enabled_generic()}
    assert ids == set(EXPECTED_WP) | set(EXPECTED_SITEMAP)


def _robots_404(base_url: str) -> None:
    respx.get(base_url.rstrip("/") + "/robots.txt").respond(404)


@pytest.mark.parametrize("source_id", sorted(EXPECTED_WP))
@respx.mock
def test_wordpress_outlet_smoke(source_id: str, make_fetcher: Callable[..., PoliteFetcher]) -> None:
    config = next(s for s in enabled_generic() if s.id == source_id)
    rec = json.loads((GENERIC / f"{source_id}_wp_posts.json").read_text(encoding="utf-8"))
    rec_q = parse_qs(urlsplit(rec["url"]).query)
    _robots_404(config.base_url)

    def answer(request: httpx.Request) -> httpx.Response:
        q = parse_qs(urlsplit(str(request.url)).query)
        if (q["search"], q["after"]) == (rec_q["search"], rec_q["after"]):
            return httpx.Response(200, json=rec["body"], headers=rec["headers"])
        return httpx.Response(200, json=[], headers={"x-wp-total": "0", "x-wp-totalpages": "0"})

    respx.get(url__startswith=config.base_url.rstrip("/") + "/wp-json/wp/v2/posts").mock(
        side_effect=answer
    )
    since = datetime.fromisoformat(rec_q["after"][0]).date() + timedelta(days=1)
    today = datetime.fromisoformat(rec_q["before"][0]).date() - timedelta(days=1)
    source = WordPressApiSource(config, make_fetcher(), GenericOptions(today=today))
    articles = list(source.list_articles(since))
    assert len(articles) == EXPECTED_WP[source_id]
    assert source.stats.errors == []
    assert all(a.source_id == source_id and a.filtro_slug is None for a in articles)
    host = urlsplit(config.base_url).netloc.removeprefix("www.")
    assert all(urlsplit(a.url).netloc.removeprefix("www.") == host for a in articles)


@pytest.mark.parametrize("source_id", sorted(EXPECTED_SITEMAP))
@respx.mock
def test_sitemap_outlet_smoke(
    source_id: str, make_fetcher: Callable[..., PoliteFetcher], tmp_path: Path
) -> None:
    config = next(s for s in enabled_generic() if s.id == source_id)
    rec = json.loads((GENERIC / f"{source_id}_pages.json").read_text(encoding="utf-8"))
    sitemap_file = next(GENERIC.glob(f"{source_id}_sitemap.xml*"))
    _robots_404(config.base_url)
    respx.get(rec["sitemap_url"]).respond(200, content=sitemap_file.read_bytes())
    for url, head in rec["pages"].items():
        respx.get(url).respond(200, text=head, headers={"content-type": "text/html; charset=utf-8"})
    if "index_url" in rec:
        index = (GENERIC / f"{source_id}_sitemap_index.xml").read_bytes()
        respx.get(rec["index_url"]).respond(200, content=index)
        month = rec["month"]
    else:
        yyyymm = re.search(r"(\d{4})(\d{2})", rec["sitemap_url"])
        assert yyyymm is not None
        month = f"{yyyymm[1]}-{yyyymm[2]}"
    options = GenericOptions(
        checkpoint_dir=tmp_path, sample_months=(month,), today=date(2026, 11, 13)
    )
    source = SitemapSource(config, make_fetcher(), options)
    if source.index_url is None:
        assert source.month_url(month) == rec["sitemap_url"]
    articles = list(source.list_articles(date(2016, 1, 1)))
    assert dict(source.stats.by_level) == EXPECTED_SITEMAP[source_id]
    assert source.stats.errors == []
    assert source.stats.units == {month: "ok"}
    assert {a.url for a in articles} == set(rec["pages"])
    assert all(a.titular and a.fecha.strftime("%Y-%m") == month for a in articles)
