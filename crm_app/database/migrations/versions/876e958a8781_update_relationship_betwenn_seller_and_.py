"""update relationship betwenn seller and contract: nulable = true

Revision ID: 876e958a8781
Revises: 9b31881e4e9a
Create Date: 2023-09-08 15:52:48.593234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '876e958a8781'
down_revision: Union[str, None] = '9b31881e4e9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contract_table', 'seller_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contract_table', 'seller_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###