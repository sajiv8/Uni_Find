from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "538812af1f7b"
down_revision: Union[str, Sequence[str], None] = "b7dd93898338"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(),
            nullable=False,
            server_default="user"
        )
    )

    op.alter_column(
        "users",
        "role",
        server_default=None
    )


def downgrade() -> None:
    op.drop_column("users", "role")