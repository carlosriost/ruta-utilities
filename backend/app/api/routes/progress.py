"""Progreso del usuario autenticado."""

from fastapi import APIRouter

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.progress import ProgressResponse
from app.services.course_service import CourseService
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/progress", tags=["Progreso"])


@router.get(
    "/me",
    response_model=ProgressResponse,
    summary="Progreso completo del operario",
    description=(
        "Porcentaje general, porcentaje por fase, nodos completados, "
        "checkpoints superados y siguiente punto disponible. Todo calculado "
        "por FastAPI a partir de PostgreSQL."
    ),
)
def read_my_progress(user: CurrentUser, db: DbSession) -> ProgressResponse:
    service = CourseService(db)
    state = service.state_for(user)
    return ProgressService(db).progress_response(user, state)
