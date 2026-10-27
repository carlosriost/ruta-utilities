"""Excepciones de dominio y su traduccion a codigos HTTP."""

from fastapi import HTTPException, status


class DomainError(HTTPException):
    """Error de negocio con un codigo HTTP explicito."""

    status_code_default = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str, status_code: int | None = None) -> None:
        super().__init__(
            status_code=status_code or self.status_code_default, detail=detail
        )


class NotFoundError(DomainError):
    status_code_default = status.HTTP_404_NOT_FOUND


class UnauthorizedError(DomainError):
    status_code_default = status.HTTP_401_UNAUTHORIZED


class NodeLockedError(DomainError):
    """El nodo existe pero todavia no esta disponible para el usuario."""

    status_code_default = status.HTTP_403_FORBIDDEN


class InvalidActivityStateError(DomainError):
    """La actividad no puede completarse todavia (faltan requisitos)."""

    status_code_default = status.HTTP_409_CONFLICT
