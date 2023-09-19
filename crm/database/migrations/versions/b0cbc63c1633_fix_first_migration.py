"""fix first migration

Revision ID: b0cbc63c1633
Revises: 029df819f48f
Create Date: 2023-09-05 11:25:18.408689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0cbc63c1633'
down_revision: Union[str, None] = '029df819f48f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
