"""Schemas Pydantic expuestos por la API."""

from app.schemas.badge import BadgeCollectionResponse, BadgeResponse
from app.schemas.course import CourseResponse, PhaseDetailResponse, PhaseResponse
from app.schemas.node import (
    NodeContentResponse,
    NodeDetailResponse,
    RequirementResponse,
    RequirementUpdateRequest,
    RequirementUpdateResponse,
)
from app.schemas.progress import (
    NodeStateResponse,
    PhaseStateResponse,
    ProgressResponse,
    ProgressSummary,
    StateChange,
)
from app.schemas.user import DemoLoginResponse, UserResponse

__all__ = [
    "BadgeCollectionResponse",
    "BadgeResponse",
    "CourseResponse",
    "DemoLoginResponse",
    "NodeContentResponse",
    "NodeDetailResponse",
    "NodeStateResponse",
    "PhaseDetailResponse",
    "PhaseResponse",
    "PhaseStateResponse",
    "ProgressResponse",
    "ProgressSummary",
    "RequirementResponse",
    "RequirementUpdateRequest",
    "RequirementUpdateResponse",
    "StateChange",
    "UserResponse",
]
