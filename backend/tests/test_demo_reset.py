"""Reinicio: borra las marcas, conserva el catalogo."""

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.badge import Badge, UserBadge
from app.models.course import Activity, CourseNode, Phase
from app.models.progress import RequirementMark, UserPhaseProgress
from app.models.user import User
from tests.helpers import PHASE_0, get_course, mark_phase


def _count(db: Session, model) -> int:
    return db.execute(select(func.count()).select_from(model)).scalar_one()


def test_reset_borra_el_avance_pero_conserva_el_curso(
    auth_client: TestClient, db: Session
) -> None:
    mark_phase(auth_client, PHASE_0, True)

    catalogo_antes = {
        "users": _count(db, User),
        "phases": _count(db, Phase),
        "nodes": _count(db, CourseNode),
        "activities": _count(db, Activity),
        "badges": _count(db, Badge),
    }
    assert _count(db, RequirementMark) > 0
    assert _count(db, UserBadge) > 0

    response = auth_client.post("/api/demo/reset")

    assert response.status_code == 200
    summary = response.json()["summary"]
    assert summary["general_progress"] == 0
    assert summary["met_requirements"] == 0
    assert summary["badges_earned"] == 0

    db.expire_all()
    # El avance desaparece...
    assert _count(db, RequirementMark) == 0
    assert _count(db, UserBadge) == 0
    # ...pero el catalogo y el usuario siguen intactos.
    catalogo_despues = {
        "users": _count(db, User),
        "phases": _count(db, Phase),
        "nodes": _count(db, CourseNode),
        "activities": _count(db, Activity),
        "badges": _count(db, Badge),
    }
    assert catalogo_despues == catalogo_antes


def test_tras_el_reset_el_mapa_vuelve_al_estado_inicial(
    auth_client: TestClient, db: Session
) -> None:
    mark_phase(auth_client, PHASE_0, True)
    auth_client.post("/api/demo/reset")

    course = get_course(auth_client)

    assert course["phases"][0]["nodes"][0]["status"] == "HAS_GAPS"
    assert course["phases"][1]["state"]["unlocked"] is False
    assert course["summary"]["next_node_id"] == course["phases"][0]["nodes"][0]["id"]
    # El snapshot de fases se regenera, no queda una fase marcada como abierta.
    db.expire_all()
    assert _count(db, UserPhaseProgress) == len(course["phases"])
