import gzip
import html
import json
from collections.abc import Callable
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest
import respx

from corredor.http import DisallowedByRobots, PoliteFetcher
from corredor.models import Article, SourceConfig
from corredor.sources.generic import (
    BAJADA_MAX_CHARS,
    GenericOptions,
    RssSource,
    SitemapSource,
    WordPressApiSource,
    decompress_if_gzip,
    parse_article_meta,
    parse_sitemap,
    plain_text,
    short_lede,
)

from .conftest import FIXTURES

BASE = "https://noticias.example"
API = f"{BASE}/wp-json/wp/v2/posts"
GENERIC = FIXTURES / "generic"
Factory = Callable[..., PoliteFetcher]


def cfg(metodo: str, **kw: object) -> SourceConfig:
    data: dict[str, object] = {
        "id": "prueba",
        "nombre": "Prueba",
        "base_url": BASE,
        "metodo": metodo,
        "tier": 1,
    }
    data.update(kw)
    return SourceConfig.model_validate(data)


def no_robots() -> None:
    respx.get(f"{BASE}/robots.txt").respond(404)


def post(pid: int, title: str, excerpt: str = "", day: str = "2025-02-03") -> dict[str, object]:
    return {
        "id": pid,
        "date": f"{day}T10:00:00",
        "link": f"{BASE}/nota-{pid}/",
        "title": {"rendered": title},
        "excerpt": {"rendered": f"<p>{excerpt}</p>"},
    }


def wp_response(posts: list[dict[str, object]], pages: int = 1) -> httpx.Response:
    headers = {"x-wp-total": str(len(posts)), "x-wp-totalpages": str(pages)}
    return httpx.Response(200, json=posts, headers=headers)


# --------------------------------------------------------------------------- helpers
def test_plain_text_decodes_and_drops_scripts() -> None:
    assert (
        plain_text("<p>Corte &amp; <b>ruta</b> 9</p><script>alert(1)</script>") == "Corte & ruta 9"
    )
    assert plain_text("&lt;script&gt;alert(1)&lt;/script&gt; x") == "<script>alert(1)</script> x"


def test_short_lede_caps_length() -> None:
    lede = short_lede("palabra " * 200)
    assert len(lede) <= BAJADA_MAX_CHARS
    assert lede.endswith("…")
    assert short_lede("Corte en Ruta 9 [&hellip;]") == "Corte en Ruta 9…"


def test_decompress_limit() -> None:
    bomb = gzip.compress(b"0" * 10_000)
    assert decompress_if_gzip(bomb, limit=20_000) == b"0" * 10_000
    with pytest.raises(ValueError, match="exceeds"):
        decompress_if_gzip(bomb, limit=1_000)
    assert decompress_if_gzip(b"<urlset/>") == b"<urlset/>"
    with pytest.raises(ValueError, match="truncated"):
        decompress_if_gzip(bomb[: len(bomb) // 2])


def test_parse_sitemap_google_news_and_cdata() -> None:
    xml = (
        '<urlset xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"><url>'
        "<loc> https://x.example/corte-ruta-9-n1 </loc><lastmod>2024-02-03T10:00:00Z</lastmod>"
        "<news:news><news:publication_date>2024-02-02</news:publication_date>"
        "<news:title><![CDATA[Corte en la Ruta 9 & más]]></news:title></news:news></url>"
        "<url><lastmod>2024</lastmod></url></urlset>"
    )
    (entry,) = parse_sitemap(xml)
    assert entry.loc == "https://x.example/corte-ruta-9-n1"
    assert entry.news_date == "2024-02-02"
    assert entry.news_title == "Corte en la Ruta 9 & más"


def test_article_meta_date_precedence() -> None:
    page = """<html><head><title>T</title>
    <meta property="og:title" content="Alud en Volcán">
    <meta property="article:published_time" content="2024-02-03T22:10:00-03:00">
    <meta itemprop="datePublished" content="2024-01-01">
    <script type="application/ld+json">{"@graph": [{"datePublished": "2023-12-31"}]}</script>
    </head><body><p>Cuerpo que nunca se lee</p></body></html>"""
    meta = parse_article_meta(page)
    assert meta.published == date(2024, 2, 3)
    assert meta.titular == "Alud en Volcán"
    ld_only = parse_article_meta(
        '<head><script type="application/ld+json">[{"headline": "H", "datePublished":'
        ' "2023-12-31T08:00:00Z"}]</script><script type="application/ld+json">{bad</script></head>'
    )
    assert (ld_only.published, ld_only.titular) == (date(2023, 12, 31), "H")
    assert parse_article_meta("<head><title>Solo título</title></head>").published is None


# --------------------------------------------------------------------------- WordPress
@respx.mock
def test_wp_searches_accent_variants_and_filters_client_side(make_fetcher: Factory) -> None:
    no_robots()
    calls: list[dict[str, list[str]]] = []

    def answer(request: httpx.Request) -> httpx.Response:
        query = parse_qs(urlsplit(str(request.url)).query)
        calls.append(query)
        if query["search"] == ["Volcán"]:
            return wp_response(
                [
                    post(1, "Alud en Volcán: cortan la Ruta 9"),
                    post(2, "Campaña de salud en Volcán"),  # 'alud' must not hit 'salud'
                ]
            )
        if query["search"] == ["Volcan"]:
            return wp_response([post(1, "Alud en Volcán: cortan la Ruta 9")])  # duplicate id
        return wp_response([])

    respx.get(API).mock(side_effect=answer)
    source = WordPressApiSource(
        cfg("wordpress_api", params={"terms": ["Volcán"]}),
        make_fetcher(),
        GenericOptions(today=date(2025, 6, 1)),
    )
    articles = list(source.list_articles(date(2025, 1, 1)))
    assert [a.url for a in articles] == [f"{BASE}/nota-1/"]
    assert [c["search"] for c in calls] == [["Volcán"], ["Volcan"]]
    assert calls[0]["_fields"] == ["id,date,link,title,excerpt"]
    assert calls[0]["after"] == ["2024-12-31T23:59:59"]
    assert calls[0]["before"] == ["2025-06-02T00:00:00"]
    art = articles[0]
    assert (art.fecha, art.fecha_fuente, art.filtro_slug) == (
        date(2025, 2, 3),
        "published_time",
        None,
    )
    assert source.stats.raw == 3
    assert source.stats.unique == 2
    assert source.stats.selected == 1


@respx.mock
def test_wp_yearly_windows_pagination_and_checkpoint(make_fetcher: Factory, tmp_path: Path) -> None:
    no_robots()
    seen: list[tuple[str, str]] = []

    def answer(request: httpx.Request) -> httpx.Response:
        q = parse_qs(urlsplit(str(request.url)).query)
        seen.append((q["after"][0][:10], q["page"][0]))
        if q["page"] == ["1"]:
            posts = [post(i, f"Corte en Purmamarca {i}") for i in range(1, 3)]
            return wp_response(posts, pages=2)
        return wp_response([post(3, "Derrumbe en la Ruta 52 en Lipán")], pages=2)

    respx.get(API).mock(side_effect=answer)
    options = GenericOptions(checkpoint_dir=tmp_path / "ck", today=date(2025, 3, 1))
    config = cfg("wordpress_api", params={"terms": ["Lipán"], "per_page": 2})
    source = WordPressApiSource(config, make_fetcher(), options)
    first = list(source.list_articles(date(2024, 5, 1)))
    # 2 years x 2 variants x 2 pages; ids repeat across windows only inside a window
    assert len(seen) == 8
    assert {a.url for a in first} == {f"{BASE}/nota-{i}/" for i in (1, 2, 3)}
    assert source.stats.units == {"2024": "ok", "2025": "ok"}
    seen.clear()
    again = WordPressApiSource(config, make_fetcher(), options)
    list(again.list_articles(date(2024, 5, 1)))
    assert again.stats.units == {"2024": "skipped", "2025": "ok"}
    assert {after for after, _ in seen} == {
        "2024-12-31"
    }  # open year 2025 re-fetched, bypassing the cache
    seen.clear()
    later = GenericOptions(checkpoint_dir=tmp_path / "ck", today=date(2026, 1, 10))
    after_rollover = WordPressApiSource(config, make_fetcher(), later)
    list(after_rollover.list_articles(date(2024, 5, 1)))
    # 2025 was collected while open: re-fetched once more, then closed for good
    assert after_rollover.stats.units == {"2024": "skipped", "2025": "ok", "2026": "ok"}
    assert {after for after, _ in seen} == {"2024-12-31", "2025-12-31"}
    assert after_rollover.checkpoint.get("2025")["closed"] is True  # type: ignore[index]


@respx.mock
def test_wp_error_marks_window_for_retry(make_fetcher: Factory, tmp_path: Path) -> None:
    no_robots()
    respx.get(API).respond(403)
    options = GenericOptions(checkpoint_dir=tmp_path, today=date(2025, 3, 1))
    source = WordPressApiSource(
        cfg("wordpress_api", params={"terms": ["Jama"]}), make_fetcher(), options
    )
    assert list(source.list_articles(date(2025, 1, 1))) == []
    assert source.stats.units == {"2025": "error"}
    assert source.stats.errors
    assert not source.checkpoint.is_done("2025")


@respx.mock
def test_wp_robots_disallow_stops_the_source(make_fetcher: Factory) -> None:
    # Same shape as jujuyaldia.com.ar: two `User-agent: *` groups, the second blocks /wp-json/.
    respx.get(f"{BASE}/robots.txt").respond(
        200, text="User-agent: *\nAllow: /\n\nUser-agent: *\nDisallow: /wp-json/\n"
    )
    api = respx.get(API).respond(200, json=[])
    source = WordPressApiSource(
        cfg("wordpress_api"), make_fetcher(), GenericOptions(today=date(2025, 3, 1))
    )
    with pytest.raises(DisallowedByRobots):
        list(source.list_articles(date(2025, 1, 1)))
    assert not api.called


@respx.mock
def test_script_headline_is_stored_as_text(make_fetcher: Factory) -> None:
    no_robots()
    payload = json.loads((GENERIC / "unsafe_wp_posts.json").read_text(encoding="utf-8"))
    respx.get(API).respond(200, json=payload)
    source = WordPressApiSource(
        cfg("wordpress_api", params={"terms": ["Jama"]}),
        make_fetcher(),
        GenericOptions(today=date(2025, 3, 1)),
    )
    (art,) = list(source.list_articles(date(2025, 1, 1)))
    assert art.titular == "<script>alert(’x’)</script> Cierran el Paso de Jama por nieve"
    assert "<img" not in art.bajada
    assert "onerror" not in art.bajada
    assert "&lt;script&gt;" in html.escape(art.titular)


# --------------------------------------------------------------------------- sitemaps
SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>{base}/jujuy/alud-en-volcan-corte-total-ruta-9-n1</loc><lastmod>2024-02-03T10:00:00Z</lastmod></url>
<url><loc>{base}/jujuy/turismo-por-la-ruta-nacional-52-n2/</loc><lastmod>2024-02-04T10:00:00Z</lastmod></url>
<url><loc>{base}/jujuy/derrumbe-en-purmamarca-corte-n3</loc><lastmod>2024-02-05T10:00:00Z</lastmod></url>
<url><loc>{base}/jujuy/feria-del-libro-n4</loc><lastmod>2024-02-06T10:00:00Z</lastmod></url>
<url><loc>https://otro.example/jujuy/alud-en-volcan-ruta-9-n5</loc></url>
</urlset>"""
HEAD = (
    '<html><head><meta property="og:title" content="{t}">'
    '<meta property="og:description" content="Bajada corta.">{d}</head><body>no</body></html>'
)


def sitemap_cfg(**kw: object) -> SourceConfig:
    return cfg("sitemap", params={"sitemap_mensual": BASE + "/sitemap-{yyyymm}.xml.gz"}, **kw)


@respx.mock
def test_sitemap_levels_dates_and_missing_pages(make_fetcher: Factory, tmp_path: Path) -> None:
    no_robots()
    respx.get(f"{BASE}/sitemap-202402.xml.gz").respond(
        200, content=gzip.compress(SITEMAP.format(base=BASE).encode())
    )
    published = '<meta property="article:published_time" content="2024-02-02T23:00:00-03:00">'
    respx.get(f"{BASE}/jujuy/alud-en-volcan-corte-total-ruta-9-n1").respond(
        200, text=HEAD.format(t="Alud en Volcán", d=published)
    )
    respx.get(f"{BASE}/jujuy/turismo-por-la-ruta-nacional-52-n2/").respond(
        200, text=HEAD.format(t="Obras en la RN 52", d="")
    )
    respx.get(f"{BASE}/jujuy/derrumbe-en-purmamarca-corte-n3").respond(404)
    feria = respx.get(f"{BASE}/jujuy/feria-del-libro-n4").respond(200, text="")
    options = GenericOptions(
        checkpoint_dir=tmp_path, sample_months=("2024-02",), today=date(2026, 1, 1)
    )
    source = SitemapSource(sitemap_cfg(), make_fetcher(), options)
    arts = {a.url.rsplit("-", 1)[-1]: a for a in source.list_articles(date(2016, 1, 1))}
    assert set(arts) == {"n1", "n2/"}
    assert (arts["n1"].filtro_slug, arts["n1"].fecha, arts["n1"].fecha_fuente) == (
        "B",
        date(2024, 2, 2),
        "published_time",
    )
    assert (arts["n2/"].filtro_slug, arts["n2/"].fecha, arts["n2/"].fecha_fuente) == (
        "C_solo_ruta",
        date(2024, 2, 4),
        "fallback",
    )
    assert arts["n1"].bajada == "Bajada corta."
    assert not feria.called  # non-selected URLs are never fetched
    st = source.stats
    assert (st.raw, st.unique, st.selected, st.pages_missing, st.offsite_skipped) == (5, 5, 2, 1, 1)
    assert st.by_level == {"B": 1, "C_solo_ruta": 1}
    assert source.checkpoint.get("2024-02")["status"] == "ok"  # type: ignore[index]


@respx.mock
def test_sitemap_month_statuses_and_resume(make_fetcher: Factory, tmp_path: Path) -> None:
    no_robots()
    respx.get(f"{BASE}/sitemap-202401.xml.gz").respond(200, text="<urlset></urlset>")
    respx.get(f"{BASE}/sitemap-202402.xml.gz").respond(404)
    feb_error = respx.get(f"{BASE}/sitemap-202403.xml.gz").respond(500)
    current = respx.get(f"{BASE}/sitemap-202404.xml.gz").respond(200, text="<urlset></urlset>")
    options = GenericOptions(checkpoint_dir=tmp_path, today=date(2024, 4, 20))
    config = sitemap_cfg(archivo_desde="2024-01-01")
    source = SitemapSource(config, make_fetcher(retries=0), options)
    assert list(source.list_articles(date(2016, 1, 1))) == []
    assert source.stats.units == {
        "2024-01": "empty",
        "2024-02": "missing",
        "2024-03": "error",
        "2024-04": "empty",
    }
    calls_error, calls_current = feb_error.call_count, current.call_count
    again = SitemapSource(config, make_fetcher(retries=0), options)
    list(again.list_articles(date(2016, 1, 1)))
    assert again.stats.units["2024-01"] == again.stats.units["2024-02"] == "skipped"
    assert feb_error.call_count > calls_error  # error month retried
    assert current.call_count == calls_current + 1  # open month re-listed, never from cache
    assert again.stats.units["2024-04"] == "empty"


@respx.mock
def test_sitemap_request_cap(make_fetcher: Factory) -> None:
    no_robots()
    respx.get(f"{BASE}/sitemap-202402.xml.gz").respond(200, text=SITEMAP.format(base=BASE))
    respx.get(url__startswith=f"{BASE}/jujuy/").respond(200, text=HEAD.format(t="x", d=""))
    options = GenericOptions(max_requests=2, sample_months=("2024-02",), today=date(2026, 1, 1))
    source = SitemapSource(sitemap_cfg(), make_fetcher(), options)
    arts = list(source.list_articles(date(2016, 1, 1)))
    assert len(arts) == 1
    assert source.stats.capped
    assert "2024-02" not in source.stats.units  # unfinished month is not checkpointed


def test_sitemap_sample_months_before_archive() -> None:
    options = GenericOptions(sample_months=("2017-01", "2024-02"), today=date(2026, 1, 1))
    source = SitemapSource(sitemap_cfg(archivo_desde="2020-01-01"), object(), options)  # type: ignore[arg-type]
    assert source.months(date(2016, 1, 1)) == ["2024-02"]
    assert source.stats.units == {"2017-01": "before_archive"}
    assert source.month_url("2024-02") == f"{BASE}/sitemap-202402.xml.gz"


def test_sitemap_requires_template() -> None:
    with pytest.raises(ValueError, match="sitemap_mensual"):
        SitemapSource(cfg("sitemap"), object())  # type: ignore[arg-type]


# --------------------------------------------------------------------------- RSS
ITEM = (
    "<item><title>{t}</title><link>{base}/{s}/</link><pubDate>{d}</pubDate>"
    "<description><![CDATA[<p>{b}</p>]]></description></item>"
)


@respx.mock
def test_rss_recorded_feed_and_filters(make_fetcher: Factory) -> None:
    feed = (GENERIC / "elsubmarino_feed.xml").read_text(encoding="utf-8")
    extra = "".join(
        [
            ITEM.format(
                t="Cortan la Ruta 9 en Volcán por un alud",
                s="a",
                d="Thu, 12 Nov 2026 10:00:00 -0300",
                b="Vialidad",
                base=BASE,
            ),
            ITEM.format(t="Alud en Volcán", s="b", d="fecha rota", b="", base=BASE),
            ITEM.format(
                t="Alud en Volcán", s="c", d="Mon, 01 Jan 2018 10:00:00 +0000", b="", base=BASE
            ),
        ]
    )
    feed = feed.replace("</channel>", extra + "</channel>")
    respx.get(f"{BASE}/robots.txt").respond(404)
    respx.get(f"{BASE}/feed/").respond(
        200, text=feed, headers={"content-type": "application/rss+xml; charset=UTF-8"}
    )
    source = RssSource(cfg("rss"), make_fetcher(), GenericOptions())
    arts = list(source.list_articles(date(2026, 1, 1)))
    assert [a.url for a in arts] == [f"{BASE}/a/"]
    assert arts[0].fecha == date(2026, 11, 12)
    assert arts[0].bajada == "Vialidad"
    assert source.stats.raw == 7  # 4 recorded items (none about the corridor) + 3 synthetic


def test_rss_feed_url_param() -> None:
    source = RssSource(cfg("rss", params={"feed_url": f"{BASE}/rss.xml"}), object())  # type: ignore[arg-type]
    assert source.feed_url() == f"{BASE}/rss.xml"


def test_articles_hold_metadata_only() -> None:
    assert set(Article.model_fields) >= {
        "url",
        "fecha",
        "fecha_fuente",
        "titular",
        "bajada",
        "filtro_slug",
    }
    assert not {"cuerpo", "texto", "body", "content"} & set(Article.model_fields)


@respx.mock
@pytest.mark.parametrize(
    "body",
    [
        b"<html><body>Mantenimiento</body></html>",
        b"<urlset><url><loc>https://noticias.example/alud-ruta-9-n1</loc></url>",
        gzip.compress(b"<urlset><url><loc>https://noticias.example/a</loc></url></urlset>")[:30],
    ],
    ids=["html", "truncated-xml", "truncated-gzip"],
)
def test_sitemap_invalid_listing_is_an_error(
    make_fetcher: Factory, tmp_path: Path, body: bytes
) -> None:
    no_robots()
    respx.get(f"{BASE}/sitemap-202402.xml.gz").respond(200, content=body)
    options = GenericOptions(
        checkpoint_dir=tmp_path, sample_months=("2024-02",), today=date(2026, 1, 1)
    )
    source = SitemapSource(sitemap_cfg(), make_fetcher(), options)
    assert list(source.list_articles(date(2016, 1, 1))) == []
    assert source.stats.units == {"2024-02": "error"}
    assert not source.checkpoint.is_done("2024-02")


@respx.mock
def test_wp_invalid_json_is_a_window_error(make_fetcher: Factory) -> None:
    no_robots()
    respx.get(API).respond(200, text="<html>no es JSON</html>")
    options = GenericOptions(today=date(2025, 3, 1))
    source = WordPressApiSource(
        cfg("wordpress_api", params={"terms": ["Jama"]}), make_fetcher(), options
    )
    assert list(source.list_articles(date(2025, 1, 1))) == []
    assert source.stats.units == {"2025": "error"}
    assert "invalid WP JSON" in source.stats.errors[0]


@respx.mock
def test_failed_requests_count_against_the_cap(make_fetcher: Factory) -> None:
    no_robots()
    route = respx.get(API).mock(side_effect=httpx.ConnectError("caído"))
    options = GenericOptions(max_requests=3, today=date(2025, 3, 1))
    source = WordPressApiSource(
        cfg("wordpress_api", params={"terms": ["Jama", "Lipán"]}), make_fetcher(retries=0), options
    )
    assert list(source.list_articles(date(2024, 1, 1))) == []
    assert source.stats.requests == 3
    assert route.call_count == 3
    assert source.stats.capped
