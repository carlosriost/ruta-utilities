"""Utilidades de la demostracion."""

from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.progress import ProgressResponse
from app.services.course_service import CourseService
from app.services.demo_service import DemoService
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/demo", tags=["Demo"])


@router.post(
    "/reset",
    response_model=ProgressResponse,
    status_code=status.HTTP_200_OK,
    summary="Reiniciar el progreso de la demostracion",
    description=(
        "Borra de PostgreSQL unicamente el avance del usuario: progreso de "
        "nodos, respuestas, progreso de fases e insignias obtenidas.\n\n"
        "NO se elimina el usuario ni la definicion del curso (fases, nodos, "
        "actividades, preguntas, opciones ni el catalogo de insignias)."
    ),
)
def reset_demo(user: CurrentUser, db: DbSession) -> ProgressResponse:
    DemoService(db).reset_progress(user)
    state = CourseService(db).state_for(user)
    return ProgressService(db).progress_response(user, state)
