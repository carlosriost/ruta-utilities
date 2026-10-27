"""Seed idempotente de la Ruta Utilities.

Uso:

    python -m app.seed
"""

from app.seed.runner import run, seed

__all__ = ["run", "seed"]
