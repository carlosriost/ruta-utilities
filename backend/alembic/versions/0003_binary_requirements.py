"""Los temas pasan a ser binarios: cumple o no cumple (defecto no cumple)

Antes un tema podia estar sin marcar, marcado MEETS o marcado FAILS. Ahora solo
existen dos estados: cumple (hay una fila en requirement_marks) o no cumple (no
hay fila). Por eso:

* se eliminan las marcas que decian explicitamente "FAILS": ese ahora es el
  valor implicito de no tener fila,
* se elimina la columna ``status``, que ya no aporta nada (toda fila que queda
  significa "cumple").

Revision ID: 0003_binary_requirements
Revises: 0002_requirement_marks
Create Date: 2026-09-21
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003_binary_requirements"
down_revision: Union[str, None] = "0002_requirement_marks"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

requirement_marks = sa.table(
    "requirement_marks", sa.column("status", sa.String)
)


def upgrade() -> None:
    # Las marcas "FAILS" se vuelven implicitas: se borran, no se migran.
    op.execute(requirement_marks.delete().where(requirement_marks.c.status == "FAILS"))
    op.drop_column("requirement_marks", "status")


def downgrade() -> None:
    op.add_column(
        "requirement_marks",
        sa.Column(
            "status", sa.String(length=16), nullable=False, server_default="MEETS"
        ),
    )
