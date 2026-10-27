"""Datos del usuario autenticado."""

from fastapi import APIRouter

from app.api.dependencies import CurrentUser
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Usuario"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Perfil del operario autenticado",
    responses={401: {"description": "Token ausente o invalido."}},
)
def read_me(user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(user)
