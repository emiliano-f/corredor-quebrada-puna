"""reports/validacion.md: candidate thresholds, absolute and per-cell percentile."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd

from corredor.calibration.thresholds import MERGED, PCT_UNIT, ThresholdCalibrator
from corredor.models import ClosureEvent, ValidationResult


def _fmt(value: object, digits: int = 1) -> str:
    return "—" if not isinstance(value, int | float) or pd.isna(value) else f"{value:.{digits}f}"


SMALL_SAMPLE = 10


def _count(value: int, n: int, test: bool) -> str:
    small = " muestra chica" if test and n < SMALL_SAMPLE else ""
    return f"{value} (n={n}{small})"


def results_table(results: Sequence[ValidationResult], percentile: bool) -> str:
    rows: dict[tuple[str, str, float], dict[str, ValidationResult]] = {}
    for r in results:
        if (r.threshold.unidad == PCT_UNIT) != percentile:
            continue
        key = (r.threshold.causa, r.threshold.variable, r.threshold.umbral)
        rows.setdefault(key, {})[r.periodo] = r
    if not rows:
        return "Sin candidatos (no hay eventos de esta causa con punto en el período de ajuste).\n"
    unit = "percentil" if percentile else "umbral"
    lines = [
        f"| causa | variable | {unit} | train aciertos | train fallos | train falsas alarmas "
        "| test aciertos | test fallos | test falsas alarmas |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for (causa, var, th), by in sorted(rows.items()):
        tr, te = by["train"], by["test"]
        label = f"p{th:g}" if percentile else f"{th:g} {tr.threshold.unidad}"
        cells = [
            _count(v, r.aciertos + r.fallos, r is te)
            for r in (tr, te)
            for v in (r.aciertos, r.fallos, r.falsas_alarmas)
        ]
        lines.append(f"| {causa} | `{var}` | {label} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def comparison_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "Sin eventos con punto en el período de ajuste.\n"
    lines = [
        "| causa | variable | días con evento | mediana con evento | mediana sin evento "
        "| percentil mediano con evento |",
        "|---|---|---|---|---|---|",
    ]
    for r in frame.itertuples():
        lines.append(
            f"| {r.causa} | `{r.variable}` | {r.dias_evento} | {_fmt(r.mediana_evento)} "
            f"| {_fmt(r.mediana_sin_evento)} | {_fmt(r.pct_mediana_evento, 0)} |"
        )
    return "\n".join(lines) + "\n"


def section(
    title: str,
    calibrator: ThresholdCalibrator,
    events: Sequence[ClosureEvent],
    features: pd.DataFrame,
) -> str:
    with_point = [e for e in events if e.punto_id]
    by_cause = {
        c: sum(1 for e in with_point if e.causa == c) for c in ("aluvion", "crecida", "nieve")
    }
    merged = ThresholdCalibrator(calibrator.train_end, calibrator.clim_start, MERGED)
    return (
        f"## {title}\n\n"
        f"Eventos con punto crítico usados: aluvión {by_cause['aluvion']}, crecida "
        f"{by_cause['crecida']} (lluvia {by_cause['aluvion'] + by_cause['crecida']}), nieve "
        f"{by_cause['nieve']}.\n\n"
        + _variant("###", calibrator, with_point, features)
        + "\n### Variante: aluvión + crecida = lluvia\n\n"
        + _variant("####", merged, with_point, features)
    )


def _variant(
    h: str,
    calibrator: ThresholdCalibrator,
    events: Sequence[ClosureEvent],
    features: pd.DataFrame,
) -> str:
    results = calibrator.candidates(events, features)
    return (
        f"{h} Variables en días con y sin evento (ajuste)\n\n"
        + comparison_table(calibrator.compare(events, features))
        + f"\n{h} Candidatos en unidades absolutas (mm / cm de ERA5)\n\n"
        + results_table(results, percentile=False)
        + f"\n{h} Candidatos en percentil por celda (climatología 2016–2022, misma estación)\n\n"
        + results_table(results, percentile=True)
    )
