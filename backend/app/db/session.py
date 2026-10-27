"""Engine, session factory y dependencia ``get_db``."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


def get_db() -> Generator[Session, None, None]:
    """Dependencia FastAPI: entrega una sesion y garantiza su cierre.

    El commit lo realizan explicitamente los servicios, de modo que una
    operacion compuesta (guardar respuesta + progreso + insignia + desbloqueo)
    ocurre dentro de una sola transaccion.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
