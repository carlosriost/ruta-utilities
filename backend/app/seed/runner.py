"""Carga idempotente del contenido en PostgreSQL.

Ejecutar tantas veces como se quiera: el seed sincroniza el catalogo con
``app/seed/content.py``. Actualiza lo que ya existe (por ``slug``), crea lo
nuevo y elimina lo que ya no forma parte del recorrido.

Las marcas de los temas que siguen existiendo NUNCA se tocan. Las de un punto
eliminado desaparecen con el (cascada en PostgreSQL), porque ese punto ya no
forma parte del recorrido.
"""

from __future__ import annotations

import logging

from sqlalchemy import delete, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import DEFAULT_UNLOCK_THRESHOLD
from app.db.session import SessionLocal
from app.models.badge import Badge
from app.models.course import Activity, CourseNode, Phase
from app.models.user import User
from app.seed.content import BADGES, PHASES

logger = logging.getLogger("ruta_utilities.seed")

# Desplazamiento temporal para reordenar sin chocar con los indices unicos.
REORDER_OFFSET = 10_000


def _seed_demo_user(db: Session) -> User:
    """Crea (o actualiza) el registro que guarda las marcas.

    La aplicacion no muestra datos personales; este usuario existe solo para
    asociar el avance mientras no haya autenticacion corporativa.
    """
    user = (
        db.query(User).filter(User.name == settings.demo_user_name).one_or_none()
        or db.query(User).order_by(User.id).first()
    )
    if user is None:
        user = User(
            name=settings.demo_user_name,
            area=settings.demo_user_area,
            plant=settings.demo_user_plant,
            role=settings.demo_user_role,
            email=settings.demo_user_email,
        )
        db.add(user)
        db.flush()
        logger.info("Registro de avance creado")
    else:
        user.name = settings.demo_user_name
        user.area = settings.demo_user_area
        user.plant = settings.demo_user_plant
        user.role = settings.demo_user_role
    return user


def _prune(db: Session) -> dict[str, int]:
    """Elimina el contenido que ya no esta en content.py."""
    phase_slugs = {phase["slug"] for phase in PHASES}
    node_slugs = {node["slug"] for phase in PHASES for node in phase["nodes"]}
    badge_slugs = {badge["slug"] for badge in BADGES}

    removed = {}
    for model, slugs in (
        (CourseNode, node_slugs),
        (Phase, phase_slugs),
        (Badge, badge_slugs),
    ):
        result = db.execute(
            delete(model)
            .where(model.slug.not_in(slugs))
            .execution_options(synchronize_session=False)
        )
        removed[model.__tablename__] = result.rowcount or 0
    db.expire_all()
    return removed


def _free_order_indexes(db: Session) -> None:
    """Aparta los order_index actuales para reasignarlos sin conflictos.

    ``phases.order_index`` y ``(phase_id, order_index)`` son unicos, asi que
    reordenar en el sitio podria chocar con una fila que aun tiene ese valor.
    """
    for model in (Phase, CourseNode):
        db.execute(
            update(model)
            .values(order_index=model.order_index + REORDER_OFFSET)
            .execution_options(synchronize_session=False)
        )
    db.expire_all()


def _seed_activity(db: Session, node: CourseNode, data: dict) -> None:
    activity = node.activity
    if activity is None:
        activity = Activity(node_id=node.id)
        db.add(activity)
        db.flush()
    activity.objective = data.get("objective", "")
    activity.body = data.get("body", "")
    activity.payload = data.get("payload")
    db.flush()


def _seed_phases(db: Session) -> None:
    for phase_data in PHASES:
        phase = db.query(Phase).filter(Phase.slug == phase_data["slug"]).one_or_none()
        if phase is None:
            phase = Phase(slug=phase_data["slug"])
            db.add(phase)
        phase.name = phase_data["name"]
        phase.description = phase_data["description"]
        phase.order_index = phase_data["order_index"]
        phase.unlock_threshold = phase_data.get(
            "unlock_threshold", DEFAULT_UNLOCK_THRESHOLD
        )
        phase.theme = phase_data.get("theme", "sky")
        phase.icon = phase_data.get("icon", "compass")
        db.flush()

        for index, node_data in enumerate(phase_data["nodes"]):
            node = (
                db.query(CourseNode)
                .filter(CourseNode.slug == node_data["slug"])
                .one_or_none()
            )
            if node is None:
                node = CourseNode(slug=node_data["slug"])
                db.add(node)
            node.phase_id = phase.id
            node.title = node_data["title"]
            node.description = node_data.get("description", "")
            node.icon = node_data.get("icon", "book")
            node.order_index = index
            node.weight = node_data["weight"]
            db.flush()
            _seed_activity(db, node, node_data["activity"])


def _seed_badges(db: Session) -> None:
    for index, badge_data in enumerate(BADGES):
        badge = db.query(Badge).filter(Badge.slug == badge_data["slug"]).one_or_none()
        if badge is None:
            badge = Badge(slug=badge_data["slug"])
            db.add(badge)
        badge.name = badge_data["name"]
        badge.description = badge_data["description"]
        badge.icon = badge_data["icon"]
        badge.theme = badge_data.get("theme", "amber")
        badge.rule_type = badge_data["rule_type"]
        badge.rule_ref = badge_data.get("rule_ref")
        badge.order_index = index
    db.flush()


def seed(db: Session) -> dict[str, int]:
    """Ejecuta el seed completo sobre una sesion existente."""
    removed = _prune(db)
    _free_order_indexes(db)
    _seed_demo_user(db)
    _seed_phases(db)
    _seed_badges(db)
    db.commit()

    summary = {
        "phases": db.query(Phase).count(),
        "nodes": db.query(CourseNode).count(),
        "activities": db.query(Activity).count(),
        "badges": db.query(Badge).count(),
    }
    if any(removed.values()):
        summary["eliminados"] = sum(removed.values())
        logger.info(
            "Contenido retirado del recorrido: %s",
            ", ".join(f"{table} {count}" for table, count in removed.items() if count),
        )
    return summary


def run() -> dict[str, int]:
    """Punto de entrada de ``python -m app.seed``."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    db = SessionLocal()
    try:
        summary = seed(db)
    finally:
        db.close()

    temas = sum(
        len(node["activity"]["payload"]["requirements"])
        for phase in PHASES
        for node in phase["nodes"]
    )
    logger.info("Seed completado. Contenido en PostgreSQL:")
    for key, value in summary.items():
        logger.info("  %-12s %s", key, value)
    logger.info("  %-12s %s", "temas", temas)
    return summary
