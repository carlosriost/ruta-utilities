"""Enumeraciones del dominio.

Se almacenan como texto en PostgreSQL (columnas VARCHAR) para que las
migraciones sean simples y el catalogo de valores pueda crecer sin ALTER TYPE.
"""

from enum import StrEnum


class NodeStatus(StrEnum):
    """Estado de un punto del mapa, derivado de sus temas.

    Un tema sin marcar CUENTA como "no cumple": no existe un tercer estado de
    "sin revisar". Por eso un punto solo puede estar bloqueado, cumplir todos
    sus temas o tener brechas (nunca "pendiente").
    """

    LOCKED = "LOCKED"
    COMPLIANT = "COMPLIANT"
    HAS_GAPS = "HAS_GAPS"


class BadgeRule(StrEnum):
    """Regla evaluada por el backend para conceder una insignia."""

    FIRST_REQUIREMENT_MET = "FIRST_REQUIREMENT_MET"
    PHASE_COMPLIANT = "PHASE_COMPLIANT"
    COURSE_COMPLIANT = "COURSE_COMPLIANT"
