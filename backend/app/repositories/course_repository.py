"""Consultas sobre la definicion del curso."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.course import Activity, CourseNode, Phase


class CourseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_phases(self) -> list[Phase]:
        """Niveles ordenados, con sus puntos precargados (evita N+1)."""
        return list(
            self.db.execute(
                select(Phase)
                .options(selectinload(Phase.nodes).selectinload(CourseNode.activity))
                .order_by(Phase.order_index)
            ).scalars()
        )

    def get_phase(self, phase_id: int) -> Phase | None:
        return self.db.get(Phase, phase_id)

    def get_phase_by_slug(self, slug: str) -> Phase | None:
        return self.db.execute(
            select(Phase).where(Phase.slug == slug)
        ).scalar_one_or_none()

    def get_node(self, node_id: int) -> CourseNode | None:
        return self.db.get(CourseNode, node_id)

    def get_node_by_slug(self, slug: str) -> CourseNode | None:
        return self.db.execute(
            select(CourseNode).where(CourseNode.slug == slug)
        ).scalar_one_or_none()

    def get_activity_for_node(self, node_id: int) -> Activity | None:
        return self.db.execute(
            select(Activity).where(Activity.node_id == node_id)
        ).scalar_one_or_none()
