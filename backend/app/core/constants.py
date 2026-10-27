"""Constantes y reglas centralizadas.

Los umbrales de cumplimiento por nivel viven en
``app/seed/vpo/builder.py`` (UNLOCK_THRESHOLDS) y se guardan en la columna
``phases.unlock_threshold``. Nunca deben escribirse sueltos en routers ni en
componentes React.
"""

#: Umbral por defecto si un nivel no declara el suyo.
DEFAULT_UNLOCK_THRESHOLD: int = 100
