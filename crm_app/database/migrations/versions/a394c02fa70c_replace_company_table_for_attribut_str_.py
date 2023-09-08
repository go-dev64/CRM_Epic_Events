"""replace Company table for attribut[str] in customer table

Revision ID: a394c02fa70c
Revises: 24b81ee088ff
Create Date: 2023-09-08 10:47:14.606844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a394c02fa70c'
down_revision: Union[str, None] = '24b81ee088ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
