"""Modelos SQLAlchemy. Importarlos aqui permite a Alembic descubrirlos todos."""

from app.db.base import Base
from app.models.badge import Badge, UserBadge
from app.models.course import Activity, CourseNode, Phase
from app.models.enums import BadgeRule, NodeStatus
from app.models.progress import RequirementMark, UserPhaseProgress
from app.models.user import User

__all__ = [
    "Activity",
    "Badge",
    "BadgeRule",
    "Base",
    "CourseNode",
    "NodeStatus",
    "Phase",
    "RequirementMark",
    "User",
    "UserBadge",
    "UserPhaseProgress",
]
