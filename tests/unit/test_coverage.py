from datetime import date
from pathlib import Path

from corredor.coverage import evaluate, is_scraped, load_control, report
from corredor.models import ClosureEvent

HEADER = (
    "id,fecha_inicio,fecha_fin,ruta,lugar_tramo,causa,tipo,confianza_fecha,lado,medios,urls,notas\n"
)
ROWS = [
    "E003,2017-01-10,2017-01-17,RN 9,Volcán,aluvión/alud,total,confirmada,n/a,La Gaceta (AR),u,",
    "E004,2017-01-17,desconocida,RN 9,Volcán (variantes),aluvión/alud,parcial,confirmada,n/a,La Gaceta (AR),u,",  # noqa: E501
    "E005,2017-01-25,2017-01-26,RN 9,Volcán,obra,total,confirmada,n/a,La Gaceta (AR),u,",
    "E029,2024-03-14,2024-03-29,RN 52,Ronqui Angosto – Saladillo,crecida,total,confirmada,n/a,Todo Jujuy (AR),u,",  # noqa: E501
    "E030,2024-03,desconocida,RN 52 – Paso de Jama (CH-27),Paso de Jama,nieve,total,aproximada,CL,El América (CL),u,",  # noqa: E501
]  # fmt: skip


def ev(fecha: date, ruta: str, punto: str | None, fin: date | None = None) -> ClosureEvent:
    return ClosureEvent(
        evento_id=f"{fecha}{punto}", fecha=fecha, ruta=ruta, punto_id=punto, causa="otro",
        tipo_corte="total", fuentes=["u"], n_medios=1, metodo="reglas", confianza="media",
        fecha_inicio=fecha, fecha_fin=fin or fecha,
    )  # fmt: skip


def control(tmp_path: Path) -> Path:
    path = tmp_path / "c.csv"
    path.write_text(HEADER + "\n".join(ROWS) + "\n", encoding="utf-8")
    return path


def test_groups_route_place_and_window(tmp_path: Path) -> None:
    rows = load_control(control(tmp_path))
    assert rows[3].puntos == {"rn52_ronqui_angosto"}
    assert rows[4].puntos == {"rn52_paso_jama"}
    assert (rows[4].inicio, rows[4].fin) == (date(2024, 3, 1), date(2024, 3, 31))
    events = [
        ev(date(2017, 1, 27), "RN9", "rn9_volcan"),  # E005 + 1 day: the Volcán unit
        ev(date(2024, 3, 10), "RN52", "rn52_ronqui_angosto", date(2024, 3, 12)),  # 14 - 2
        ev(date(2024, 3, 20), "RN52", "rn52_susques"),  # other point: no match
    ]
    found = {u.id: u for u in evaluate(rows, events)}
    assert set(found) == {"E003–E005", "E029", "E030"}
    assert len(found["E003–E005"].matches) == 1
    assert len(found["E029"].matches) == 1
    assert found["E030"].matches == []
    text = report(list(found.values()), ["Todo Jujuy", "El Submarino Jujuy"])
    assert "| todos | 2/3 (67%) | 2/3 (67%) |" in text
    assert "| fecha aproximada | 0/1 (0%) | 0/1 (0%) |" in text
    assert "| solo medios que recolectamos | 1/1 (100%) | 1/1 (100%) |" in text
    assert "| E030 |" in text


def test_point_less_event_matches_on_route_and_date(tmp_path: Path) -> None:
    rows = load_control(control(tmp_path))
    found = evaluate(rows, [ev(date(2024, 3, 16), "RN52", None)])
    assert [u.id for u in found if u.matches] == ["E029", "E030"]  # optimistic
    assert [u.id for u in found if u.strict] == []  # strict: both have a place


def test_is_scraped() -> None:
    names = ["todo jujuy", "el tribuno de jujuy"]
    assert is_scraped("El Tribuno", names)
    assert is_scraped("Todo Jujuy", names)
    assert not is_scraped("La Gaceta", names)
