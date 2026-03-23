"""alter hashed_password nullable

Revision ID: alter_password
Revises: add_is_active
Create Date: 2026-03-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'alter_password'
down_revision: Union[str, None] = 'add_is_active'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'hashed_password', nullable=True)


def downgrade() -> None:
    op.alter_column('users', 'hashed_password', nullable=False)
