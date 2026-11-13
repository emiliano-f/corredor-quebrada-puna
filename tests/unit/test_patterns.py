import pytest

from corredor.extraction import patterns as p


@pytest.mark.parametrize(
    ("text", "route"),
    [
        ("Ruta Nacional Nº 52 cortada", "RN52"),
        ("Corte total en la ruta nro 52", "RN52"),
        ("Ruta Nacional número 9: tránsito lento", "RN9"),
        ("ruta nacional N° 9 en Volcán", "RN9"),
        ("Ruta Nac. 52 habilitada", "RN52"),
        ("RN52 intransitable", "RN52"),
        ("rn 9 a la altura de Tumbaya", "RN9"),
        ("ruta-nacional-9-cortada", "RN9"),
    ],
)
def test_route_forms(text: str, route: str) -> None:
    assert route in p.routes(text)


@pytest.mark.parametrize("text", ["Ruta 90 en Salta", "ruta 520", "ruta provincial 16"])
def test_route_no_false_numbers(text: str) -> None:
    assert p.routes(text) == set()


def test_route_52_cortada_is_candidate() -> None:
    text = "Ruta Nacional Nº 52 cortada"
    assert p.is_closure(text)
    assert p.is_candidate(text)


@pytest.mark.parametrize(
    "text",
    [
        "Cierran el Paso de Jama",
        "Cortaron la ruta 9 en Volcán",
        "Cortan el tránsito en Purmamarca",
        "Cerraron el paso por nevadas",
        "Vialidad cerró la Cuesta de Lipán",
        "Tránsito interrumpido en Tumbaya",
        "Cuesta de Lipán: ruta intransitable",
    ],
)
def test_closure_verbs(text: str) -> None:
    assert p.is_closure(text)


@pytest.mark.parametrize("text", ["Habilitaron el Paso de Jama", "Reabren la ruta 52"])
def test_reopening(text: str) -> None:
    assert p.is_reopening(text)
    assert p.is_candidate(text)


def test_viento_blanco_en_jama() -> None:
    text = "Viento blanco en Jama"
    assert "nieve" in p.causes(text)
    assert p.is_candidate(text)


def test_temporal_cierran_jama() -> None:
    text = "Temporal: cierran Jama"
    assert "meteo_generico" in p.causes(text)
    assert p.is_closure(text)


def test_corte_suprema_is_not_closure() -> None:
    text = "La Corte Suprema falló sobre tierras en Purmamarca"
    assert not p.is_closure(text)
    assert not p.is_candidate(text)


@pytest.mark.parametrize(
    "text",
    [
        "Corte de luz en Tilcara",
        "Corte de agua programado en Maimará",
        "Corte de cinta en el nuevo hospital de Humahuaca",
        "Cierre de campaña en Tilcara",
        "Cierre de temporada en Purmamarca",
        "Cierre del festival en Humahuaca",
    ],
)
def test_negative_phrases(text: str) -> None:
    assert not p.is_closure(text)
    assert not p.is_candidate(text)


def test_negative_does_not_hide_real_closure() -> None:
    assert p.is_closure("Tras el corte de luz, cortan la ruta 9 en Tilcara")


def test_salud_is_not_alud() -> None:
    text = "Salud: operativo en Tilcara"
    assert "aluvion" not in p.causes(text)
    assert not p.term_regex("alud").search(p.norm(text))
    assert p.term_regex("alud").search(p.norm("Un alud cortó la ruta"))
    assert p.term_regex("alud").search(p.norm("aludes en Volcán"))


def test_cerro_is_not_closure() -> None:
    assert not p.is_closure("Cerro de los Siete Colores")
    assert not p.is_closure("Los cerros de Purmamarca")


def test_foreign_volcano_is_not_corridor() -> None:
    assert not p.is_corridor("Erupción del volcán Láscar")
    assert not p.is_corridor("El volcán Villarrica en alerta")
    assert p.is_corridor("Alud en Volcán")


def test_accident_needs_closure_term() -> None:
    assert "accidente" not in p.causes("Accidente en la ruta 9")
    assert "accidente" in p.causes("Vuelco de camión: cortan la ruta 52")


@pytest.mark.parametrize(
    ("text", "group"),
    [
        ("Aluvión en Volcán", "aluvion"),
        ("Crecida del río Grande", "crecida"),
        ("Nevadas en Abra de Potrerillos", "nieve"),
        ("Piquete en la ruta 9", "protesta"),
        ("Bacheo en la ruta 52", "obra"),
        ("Granizo en Susques", "meteo_generico"),
    ],
)
def test_cause_groups(text: str, group: str) -> None:
    assert group in p.causes(text)


def test_search_variants() -> None:
    assert p.search_variants("Lipán") == ["Lipán", "Lipan"]
    assert p.search_variants("Jama") == ["Jama"]


@pytest.mark.parametrize(
    ("url", "level"),
    [
        ("https://www.todojujuy.com/jujuy/alud-en-volcan-corte-ruta-9-n123456/", "B"),
        ("https://x.com/sociedad/cuesta-de-lipan-intransitable", "B"),
        ("https://x.com/seguridad-vial/ruta-nacional-52-km-60-transito", "B"),
        ("https://x.com/jujuy/obras-en-la-ruta-9-avanzan-n9999999", "B"),
        ("https://x.com/turismo/ruta-9-nuevo-parador-n9999999", "C_solo_ruta"),
        ("https://x.com/jujuy/ruta-52-nuevo-mirador/", "C_solo_ruta"),
        ("https://x.com/deportes/gimnasia-gano-n12345", None),
        ("https://x.com/salud/operativo-en-tilcara/", None),
    ],
)
def test_slug_level(url: str, level: str | None) -> None:
    assert p.slug_level(url) == level


def test_url_text_trailing_slash_and_full_path() -> None:
    assert p.url_text("https://x.com/seguridad-vial/corte-en-lipan/") == (
        "seguridad vial corte en lipan"
    )


def test_wp_search_terms_are_specific() -> None:
    assert "alud" in p.WP_SEARCH_TERMS
    assert not {"ruta 9", "corte"} & set(p.WP_SEARCH_TERMS)
    assert all(p.term_regex(t).search(p.norm(t)) for t in p.WP_SEARCH_TERMS)


def test_ministry_name_does_not_swallow_the_sentence() -> None:
    text = "Ministerio de Infraestructura informó cortes en la ruta 9 por derrumbes"
    assert p.is_candidate(text)
    assert "obra" not in p.causes(text)
