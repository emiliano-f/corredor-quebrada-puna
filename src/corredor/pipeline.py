"""Pipeline orchestration and the `corredor` CLI (typer). User-facing text in Spanish."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from corredor import __version__
from corredor.config import Settings, load_config
from corredor.http import PoliteFetcher
from corredor.reports import lineage, write_manifest
from corredor.sources.jama import append_jsonl, build_collectors

app = typer.Typer(
    help="Corredor Quebrada–Puna: catálogo de cortes y alertas para RN 9 y RN 52.",
    no_args_is_help=True,
    add_completion=False,
)

NOT_READY_EXIT = 2


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version", callback=_version_callback, is_eager=True, help="Muestra la versión."
        ),
    ] = False,
) -> None:
    """Corredor Quebrada–Puna."""


def _not_ready(stage: str) -> None:
    typer.echo(f"La etapa '{stage}' todavía no está implementada.", err=True)
    raise typer.Exit(NOT_READY_EXIT)


ConfigOpt = Annotated[Path | None, typer.Option("--config", help="Ruta a config.yaml.")]


@app.command()
def manifest(config: ConfigOpt = None) -> None:
    """Escribe data/manifest.json (versión, commit, SCHEMA_VERSION, hash de fuentes)."""
    settings = Settings()
    cfg = load_config(config or settings.config_path)
    path = write_manifest(settings.data_dir, lineage(cfg))
    typer.echo(f"Manifiesto escrito en {path}")


@app.command()
def datos() -> None:
    """Recolecta artículos, extrae eventos y carga clima."""
    _not_ready("datos")


@app.command()
def calibrar() -> None:
    """Calibra umbrales por causa y escribe reports/validacion.md."""
    _not_ready("calibrar")


@app.command()
def precision() -> None:
    """Lee reports/revision_manual.csv y reporta la precisión por campo."""
    _not_ready("precision")


@app.command()
def reporte() -> None:
    """Genera reports/calidad_catalogo.md."""
    _not_ready("reporte")


DEFAULT_JAMA_OUT = Path("snapshots/jama_estado.jsonl")


@app.command("snapshot-jama")
def snapshot_jama(
    config: ConfigOpt = None,
    salida: Annotated[
        Path, typer.Option("--salida", help="Archivo JSONL al que se agregan las líneas.")
    ] = DEFAULT_JAMA_OUT,
) -> None:
    """Guarda el estado actual del Paso de Jama en snapshots/jama_estado.jsonl.

    Una request por fuente; si una fuente falla se guarda la línea con `error` y el
    comando termina igual con código 0.
    """
    settings = Settings()
    cfg = load_config(config or settings.config_path)
    fetcher = PoliteFetcher(
        cfg.http.user_agent,
        settings.cache_dir,
        min_interval_s=cfg.http.min_interval_s,
        timeout_s=cfg.http.timeout_s,
        retries=cfg.http.retries,
        robots_ttl_s=cfg.http.robots_ttl_h * 3600,
        not_found_ttl_s=cfg.http.not_found_ttl_h * 3600,
    )
    try:
        rows = [collector.snapshot() for collector in build_collectors(cfg.fuentes, fetcher)]
    finally:
        fetcher.close()
    if not rows:
        typer.echo("No hay fuentes de snapshot de Jama habilitadas en la configuración.", err=True)
        raise typer.Exit(1)
    append_jsonl(salida, rows)
    for row in rows:
        estado = f"error: {row.error}" if row.error else "ok"
        typer.echo(f"{row.fuente} {row.fetched_at.isoformat()} {estado}")
    typer.echo(f"{len(rows)} línea(s) agregada(s) a {salida}")


if __name__ == "__main__":  # pragma: no cover
    app()
