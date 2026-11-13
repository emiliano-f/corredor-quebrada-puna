"""Corredor Quebrada–Puna: road-closure catalog and risk alerts for RN 9 and RN 52 (Jujuy)."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("corredor")
except PackageNotFoundError:  # pragma: no cover - only when running from an uninstalled tree
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
