"""empty message

Revision ID: d2b17392126b
Revises: 4ebad65dd9b0
Create Date: 2025-02-19 22:20:13.831036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2b17392126b'
down_revision: Union[str, None] = '4ebad65dd9b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
