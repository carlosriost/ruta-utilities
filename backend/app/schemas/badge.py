"""Schemas de insignias."""

from datetime import datetime

from pydantic import BaseModel


class BadgeResponse(BaseModel):
    """Insignia con el estado de obtencion del usuario actual."""

    id: int
    slug: str
    name: str
    description: str
    icon: str
    theme: str
    earned: bool = False
    awarded_at: datetime | None = None


class BadgeCollectionResponse(BaseModel):
    """Coleccion completa de insignias del usuario."""

    badges: list[BadgeResponse]
    earned: int
    total: int
