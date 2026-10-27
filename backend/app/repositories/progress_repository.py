"""Consultas y escrituras sobre las marcas de los temas.

Un tema es binario: cumple o no cumple, con "no cumple" como valor por
defecto. Por eso solo se persiste la excepcion (los que cumplen); no existe un
tercer estado de "sin marcar".
"""

from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.progress import RequirementMark, UserPhaseProgress


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ProgressRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # --- Marcas de temas ---------------------------------------------------
    def met_codes(self, user_id: int) -> dict[str, RequirementMark]:
        """Codigos de los temas que la persona marco como cumplidos."""
        marks = self.db.execute(
            select(RequirementMark).where(RequirementMark.user_id == user_id)
        ).scalars()
        return {mark.code: mark for mark in marks}

    def mark_as_met(self, user_id: int, node_id: int, code: str) -> RequirementMark:
        existing = self.db.execute(
            select(RequirementMark).where(
                RequirementMark.user_id == user_id, RequirementMark.code == code
            )
        ).scalar_one_or_none()
        if existing is not None:
            return existing
        mark = RequirementMark(user_id=user_id, node_id=node_id, code=code)
        self.db.add(mark)
        self.db.flush()
        return mark

    def unmark(self, user_id: int, code: str) -> None:
        """Vuelve el tema a "no cumple" (el valor por defecto)."""
        self.db.execute(
            delete(RequirementMark).where(
                RequirementMark.user_id == user_id, RequirementMark.code == code
            )
        )
        self.db.flush()

    # --- Estado por nivel --------------------------------------------------
    def phase_progress_map(self, user_id: int) -> dict[int, UserPhaseProgress]:
        records = self.db.execute(
            select(UserPhaseProgress).where(UserPhaseProgress.user_id == user_id)
        ).scalars()
        return {record.phase_id: record for record in records}

    def get_or_create_phase_progress(
        self, user_id: int, phase_id: int
    ) -> UserPhaseProgress:
        record = self.db.execute(
            select(UserPhaseProgress).where(
                UserPhaseProgress.user_id == user_id,
                UserPhaseProgress.phase_id == phase_id,
            )
        ).scalar_one_or_none()
        if record is None:
            record = UserPhaseProgress(user_id=user_id, phase_id=phase_id)
            self.db.add(record)
            self.db.flush()
        return record

    # --- Reinicio ----------------------------------------------------------
    def delete_all_progress(self, user_id: int) -> None:
        """Borra unicamente el avance del usuario, nunca el catalogo."""
        self.db.execute(
            delete(RequirementMark).where(RequirementMark.user_id == user_id)
        )
        self.db.execute(
            delete(UserPhaseProgress).where(UserPhaseProgress.user_id == user_id)
        )
