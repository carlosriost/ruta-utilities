"""Schemas de usuario y autenticacion."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    """Datos publicos del operario."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(examples=["Carlos Rios"])
    area: str = Field(examples=["Utilities"])
    plant: str = Field(examples=["Cerveceria Itagui"])
    role: str = Field(examples=["Operario"])
    email: str | None = None
    created_at: datetime


class DemoLoginResponse(BaseModel):
    """Respuesta del login de demostracion."""

    access_token: str = Field(
        description="Token opaco de sesion demo. Enviar en 'Authorization: Bearer <token>'."
    )
    token_type: str = "bearer"
    auth_provider: str = Field(description="Proveedor de identidad activo.")
    user: UserResponse
