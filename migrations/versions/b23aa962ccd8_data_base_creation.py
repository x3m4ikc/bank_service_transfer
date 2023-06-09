"""Data base creation

Revision ID: b23aa962ccd8
Revises: 
Create Date: 2023-03-23 15:01:15.538665

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b23aa962ccd8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "payee",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "INDIVIDUALS",
                "INDIVIDUAL_ENTEPRENEURS",
                "ORGANIZATIONS",
                name="typepayee",
            ),
            nullable=True,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("INN", sa.String(length=12), nullable=False),
        sa.Column("BIC", sa.String(length=9), nullable=False),
        sa.Column("payee_account_number", sa.String(length=255), nullable=False),
        sa.Column("payee_card_number", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "template_for_payment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("payee_name", sa.String(length=255), nullable=False),
        sa.Column("payee_account_number", sa.String(length=30), nullable=False),
        sa.Column("template_purpose_of_payment", sa.String(length=255), nullable=False),
        sa.Column("BIC", sa.String(length=9), nullable=False),
        sa.Column("INN", sa.String(length=12), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "transfer_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type_name", sa.String(length=255), nullable=False),
        sa.Column("currency_code", sa.String(), nullable=False),
        sa.Column("min_commission", sa.Numeric(), nullable=False),
        sa.Column("max_commission", sa.Numeric(), nullable=False),
        sa.Column("percent_commission", sa.Numeric(), nullable=True),
        sa.Column("commission_fix", sa.Numeric(), nullable=False),
        sa.Column("min_sum", sa.Numeric(), nullable=False),
        sa.Column("max_sum", sa.Numeric(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "additional_parameteres",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("payee_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["payee_id"],
            ["payee.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "transfer_order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.Date(), nullable=False),
        sa.Column("transfer_type_id", sa.Integer(), nullable=False),
        sa.Column("purpose", sa.String(), nullable=False),
        sa.Column("remitter_card_number", sa.String(length=16), nullable=False),
        sa.Column("payee_id", sa.Integer(), nullable=False),
        sa.Column("sum", sa.Numeric(), nullable=False),
        sa.Column("sum_commission", sa.Numeric(), nullable=False),
        sa.Column("completed_at", sa.Date(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "DRAFT", "IN_PROGRESS", "PERFORMED", "REJECTED", name="transferstatus"
            ),
            nullable=False,
        ),
        sa.Column("authorization_code", sa.String(length=255), nullable=False),
        sa.Column("currency_exchange", sa.Numeric(), nullable=False),
        sa.Column("is_favorite", sa.Boolean(), nullable=False),
        sa.Column("start_date", sa.String(), nullable=True),
        sa.Column("periodicity", sa.String(), nullable=True),
        sa.Column("client_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["payee_id"],
            ["payee.id"],
        ),
        sa.ForeignKeyConstraint(
            ["transfer_type_id"],
            ["transfer_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transfer_order")
    op.drop_table("additional_parameteres")
    op.drop_table("transfer_type")
    op.drop_table("template_for_payment")
    op.drop_table("payee")
    # ### end Alembic commands ###
