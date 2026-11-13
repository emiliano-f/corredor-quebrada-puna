"""Pipeline orchestration and the `corredor` CLI (typer). User-facing text in Spanish."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from corredor import __version__
from corredor.config import Settings, load_config
from corredor.reports import lineage, write_manifest

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


@app.command("snapshot-jama")
def snapshot_jama() -> None:
    """Guarda el estado actual del Paso de Jama en snapshots/jama_estado.jsonl."""
    _not_ready("snapshot-jama")


if __name__ == "__main__":  # pragma: no cover
    app()
