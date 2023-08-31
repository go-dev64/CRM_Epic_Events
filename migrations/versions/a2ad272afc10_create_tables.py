"""Create tables

Revision ID: a2ad272afc10
Revises: 
Create Date: 2023-08-30 18:23:13.736768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a2ad272afc10"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "address_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("street", sa.String(length=500), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("postal_code", sa.Integer(), nullable=False),
        sa.Column("country", sa.String(length=50), nullable=False),
        sa.Column("note", sa.String(length=2048), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "company_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("phone_number", sa.String(length=12), nullable=True),
        sa.Column("number_of_employee", sa.Integer(), nullable=False),
        sa.Column("address_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["address_id"],
            ["company_table.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "manager_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("email_address", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=10), nullable=True),
        sa.Column("created_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email_address"),
    )
    op.create_table(
        "seller_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("email_address", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=10), nullable=True),
        sa.Column("created_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email_address"),
    )
    op.create_table(
        "supporter_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("email_address", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=10), nullable=True),
        sa.Column("created_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email_address"),
    )
    op.create_table(
        "customer_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("email_address", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=12), nullable=True),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.Column("created_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("seller_contact_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company_table.id"],
        ),
        sa.ForeignKeyConstraint(
            ["seller_contact_id"],
            ["seller_table.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "contract_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("total_amount", sa.Integer(), nullable=False),
        sa.Column("remaining", sa.Integer(), nullable=False),
        sa.Column("created_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("signed_contract", sa.Boolean(), nullable=False),
        sa.Column("seller_id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customer_table.id"],
        ),
        sa.ForeignKeyConstraint(
            ["seller_id"],
            ["seller_table.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "event_table",
        sa.Column("date_start", sa.DateTime(), nullable=False),
        sa.Column("date_end", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("attendees", sa.Integer(), nullable=False),
        sa.Column("note", sa.String(length=2048), nullable=True),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("contract_id", sa.Integer(), nullable=False),
        sa.Column("supporter_id", sa.Integer(), nullable=True),
        sa.Column("address_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["address_id"],
            ["address_table.id"],
        ),
        sa.ForeignKeyConstraint(
            ["contract_id"],
            ["contract_table.id"],
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customer_table.id"],
        ),
        sa.ForeignKeyConstraint(
            ["supporter_id"],
            ["supporter_table.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("event_table")
    op.drop_table("contract_table")
    op.drop_table("customer_table")
    op.drop_table("supporter_table")
    op.drop_table("seller_table")
    op.drop_table("manager_table")
    op.drop_table("company_table")
    op.drop_table("address_table")
    # ### end Alembic commands ###
