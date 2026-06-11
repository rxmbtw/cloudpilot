"""add user role

Revision ID: 1ff7a0ff6592
Revises: b97119a3983d
Create Date: 2026-06-11 10:26:26.816287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ff7a0ff6592'
down_revision: Union[str, Sequence[str], None] = 'b97119a3983d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(),
            nullable=False,
            server_default="user"
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "role")
