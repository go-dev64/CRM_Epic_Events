"""test non concluant retour

Revision ID: e7a069ee03e1
Revises: 5c863a904152
Create Date: 2023-09-18 14:31:41.367317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7a069ee03e1'
down_revision: Union[str, None] = '5c863a904152'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contract_table', sa.Column('seller_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contract_table', 'seller_table', ['seller_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contract_table', type_='foreignkey')
    op.drop_column('contract_table', 'seller_id')
    # ### end Alembic commands ###