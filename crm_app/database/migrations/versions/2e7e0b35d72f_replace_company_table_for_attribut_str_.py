"""replace Company table for attribut[str] in customer table

Revision ID: 2e7e0b35d72f
Revises: a394c02fa70c
Create Date: 2023-09-08 10:52:23.523027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e7e0b35d72f'
down_revision: Union[str, None] = 'a394c02fa70c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
