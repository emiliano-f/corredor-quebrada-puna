"""Coverage of the catalog against a hand-built control list (reports/control/).

The control list is read only here, to measure recall; it never enters the pipeline tables.
Matching: same route, same place (or an event without point), and the event's
[fecha_inicio, fecha_fin] overlapping the control dates widened by ±`window_days`.
"""

from __future__ import annotations

import calendar
import csv
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

from corredor.extraction import patterns as p
from corredor.extraction.rules import JAMA_POINT, PLACE_POINTS
from corredor.models import ClosureEvent

_KM = re.compile(r"\bkm ?\d")
GROUPS: tuple[tuple[str, ...], ...] = (("E003", "E004", "E005"),)  # Volcán, Jan 2017


@dataclass(frozen=True)
class ControlRow:
    id: str
    inicio: date
    fin: date
    rutas: frozenset[str]
    puntos: frozenset[str]
    lugar: str
    confirmada: bool
    medios: tuple[str, ...]
    localizado: bool = False  # a place, a km or Jama is named: strict needs a located event


@dataclass
class Unit:
    """One control event (or a group of rows counted as one)."""

    rows: list[ControlRow]
    matches: list[ClosureEvent] = field(default_factory=list)
    strict: list[ClosureEvent] = field(default_factory=list)

    @property
    def id(self) -> str:
        ids = [r.id for r in self.rows]
        return ids[0] if len(ids) == 1 else f"{ids[0]}–{ids[-1]}"

    @property
    def confirmada(self) -> bool:
        return all(r.confirmada for r in self.rows)

    @property
    def medios(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(m for r in self.rows for m in r.medios))


def _dates(start: str, end: str) -> tuple[date, date]:
    if len(start) == 7:  # year-month only
        y, m = map(int, start.split("-"))
        lo, hi = date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1])
    else:
        lo = hi = date.fromisoformat(start)
    if end and end[0].isdigit():
        hi = max(hi, date.fromisoformat(end))
    return lo, hi


def _route_points(ruta: str, lugar: str) -> tuple[frozenset[str], frozenset[str]]:
    r = p.norm(ruta)
    rutas = {name for num, name in (("9", "RN9"), ("52", "RN52")) if f"rn {num}" in r}
    puntos = {PLACE_POINTS[pl] for pl in p.places(lugar) if pl in PLACE_POINTS}
    if "jama" in r:
        puntos = {JAMA_POINT}
    return frozenset(rutas), frozenset(puntos)


def _located(puntos: frozenset[str], lugar: str) -> bool:
    return bool(puntos or p.places(lugar) or _KM.search(p.norm(lugar)))


def load_control(path: Path) -> list[ControlRow]:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for row in rows:
        lo, hi = _dates(row["fecha_inicio"].strip(), row["fecha_fin"].strip())
        rutas, puntos = _route_points(row["ruta"], row["lugar_tramo"])
        medios = tuple(
            m.split("(")[0].strip()
            for part in row["medios"].split(";")
            for m in part.split("/")
            if m.strip()
        )
        out.append(
            ControlRow(
                row["id"], lo, hi, rutas, puntos, row["lugar_tramo"],
                row["confianza_fecha"].strip() == "confirmada", medios,
                _located(puntos, row["lugar_tramo"]),
            )
        )  # fmt: skip
    return out


def units(rows: Sequence[ControlRow], groups: Iterable[Sequence[str]] = GROUPS) -> list[Unit]:
    by_id = {r.id: r for r in rows}
    grouped = {i for g in groups for i in g}
    out = [Unit([by_id[i] for i in g if i in by_id]) for g in groups]
    out = [u for u in out if u.rows]
    out += [Unit([r]) for r in rows if r.id not in grouped]
    return sorted(out, key=lambda u: u.rows[0].id)


def matches(row: ControlRow, ev: ClosureEvent, window_days: int = 2, strict: bool = False) -> bool:
    """Strict: an event without point does not match a control event with a known place."""
    if ev.ruta not in row.rutas:
        return False
    lo, hi = row.inicio - timedelta(days=window_days), row.fin + timedelta(days=window_days)
    start, end = ev.fecha_inicio or ev.fecha, ev.fecha_fin or ev.fecha
    if end < lo or start > hi:
        return False
    if ev.punto_id is None:
        return not (strict and row.localizado)
    return not row.puntos or ev.punto_id in row.puntos


def is_scraped(medio: str, outlets: Iterable[str]) -> bool:
    m = p.norm(medio).strip()
    return any(m == o or (len(m) >= 8 and (m in o or o in m)) for o in outlets)


def evaluate(
    control: Sequence[ControlRow], events: Sequence[ClosureEvent], window_days: int = 2
) -> list[Unit]:
    out = units(control)
    for u in out:
        u.matches = [e for e in events if any(matches(r, e, window_days) for r in u.rows)]
        u.strict = [e for e in u.matches if any(matches(r, e, window_days, True) for r in u.rows)]
    return out


def _rate(sel: Sequence[Unit], strict: bool = False) -> str:
    hit = sum(1 for u in sel if (u.strict if strict else u.matches))
    return f"{hit}/{len(sel)} ({hit / len(sel):.0%})" if sel else "0/0"


def _rates(sel: Sequence[Unit]) -> str:
    return f"{_rate(sel)} | {_rate(sel, strict=True)}"


def report(found: Sequence[Unit], outlets: Iterable[str]) -> str:
    names = [p.norm(o).strip() for o in outlets]
    only = [u for u in found if u.medios and all(is_scraped(m, names) for m in u.medios)]
    other = [u for u in found if u not in only]
    lines = [
        "Optimista: un evento sin punto cuenta para un evento de control con lugar. Estricta: "
        "no cuenta.",
        "",
        "| grupo | optimista: cubiertos / n (%) | estricta: cubiertos / n (%) |",
        "|---|---|---|",
        f"| todos | {_rates(found)} |",
        f"| fecha confirmada | {_rates([u for u in found if u.confirmada])} |",
        f"| fecha aproximada | {_rates([u for u in found if not u.confirmada])} |",
        f"| solo medios que recolectamos | {_rates(only)} |",
        f"| algún medio que no recolectamos | {_rates(other)} |",
        "",
        "## Faltantes (optimista)",
        "",
        "| id | fecha | ruta | lugar | medios |",
        "|---|---|---|---|---|",
    ]
    for u in found:
        if not u.matches:
            r = u.rows[0]
            rutas = "/".join(sorted(r.rutas))
            lines.append(f"| {u.id} | {r.inicio} | {rutas} | {r.lugar} | {'; '.join(u.medios)} |")
    loose = [u for u in found if u.matches and not u.strict]
    lines += ["", "## Cubiertos solo con eventos sin punto (faltan en la estricta)", ""]
    lines += [f"- {u.id}: {u.rows[0].lugar}" for u in loose] or ["- ninguno"]
    lines += ["", "## Coincidencias", "", "| id | eventos del catálogo |", "|---|---|"]
    for u in found:
        if u.matches:
            evs = ", ".join(
                f"{e.fecha_inicio or e.fecha}→{e.fecha_fin or e.fecha} {e.punto_id or 'sin punto'}"
                for e in u.matches
            )
            lines.append(f"| {u.id} | {evs} |")
    return "\n".join(lines) + "\n"
