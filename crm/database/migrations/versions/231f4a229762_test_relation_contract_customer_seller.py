"""test relation contract/customer/seller

Revision ID: 231f4a229762
Revises: c9a920f6caed
Create Date: 2023-09-18 11:47:48.941593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '231f4a229762'
down_revision: Union[str, None] = 'c9a920f6caed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('contract_table_seller_id_fkey', 'contract_table', type_='foreignkey')
    op.drop_column('contract_table', 'seller_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contract_table', sa.Column('seller_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('contract_table_seller_id_fkey', 'contract_table', 'seller_table', ['seller_id'], ['id'])
    # ### end Alembic commands ###