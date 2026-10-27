"""Punto de entrada de la API de Ruta Utilities.

Aqui solo se ensambla la aplicacion: configuracion, CORS, manejo de errores y
registro de routers. La logica vive en ``app/services``.
"""

import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import auth, badges, course, demo, nodes, progress, users
from app.core.config import settings
from app.db.session import engine

logger = logging.getLogger("ruta_utilities")

DESCRIPTION = """
API de **Ruta Utilities**, el recorrido de aprendizaje gamificado del area de
Utilities.

FastAPI es el responsable de las reglas del juego:

* calcula el progreso ponderado por fase y el general,
* decide que puntos estan bloqueados, disponibles o completados,
* valida las respuestas contra PostgreSQL,
* aplica la regla de desbloqueo de fases,
* concede las insignias.

React unicamente representa el estado que recibe.

**Como probar desde Swagger**

1. Ejecuta `POST /api/auth/demo-login`.
2. Copia el `access_token` de la respuesta.
3. Pulsa **Authorize** (arriba a la derecha) y pegalo.
4. Ya puedes llamar al resto de endpoints.
"""

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Autenticacion", "description": "Login de demostracion."},
        {"name": "Usuario", "description": "Perfil del operario."},
        {"name": "Curso", "description": "Mapa, fases y nodos."},
        {"name": "Puntos del recorrido", "description": "Abrir, contestar y completar."},
        {"name": "Progreso", "description": "Porcentajes y siguiente punto."},
        {"name": "Insignias", "description": "Logros del operario."},
        {"name": "Demo", "description": "Reinicio del progreso de la demo."},
    ],
    contact={"name": "Ruta Utilities - demo interna"},
)

# CORS acotado: solo el frontend de desarrollo, nunca "*".
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(_: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Nunca se devuelve un stack trace de Python al navegador."""
    logger.exception("Error de base de datos", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": (
                "No pudimos comunicarnos con la base de datos. "
                "Verifica que PostgreSQL este en ejecucion."
            )
        },
    )


@app.get("/", tags=["Demo"], summary="Informacion basica del servicio")
def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": app.version,
        "docs": "/docs",
        "redoc": "/redoc",
        "api": settings.api_prefix,
        "auth_provider": settings.auth_provider,
    }


@app.get("/health", tags=["Demo"], summary="Estado del servicio y de PostgreSQL")
def health() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        database = "ok"
    except SQLAlchemyError:
        database = "unavailable"
    return {"status": "ok", "database": database, "environment": settings.app_env}


for module in (auth, users, course, nodes, progress, badges, demo):
    app.include_router(module.router, prefix=settings.api_prefix)
