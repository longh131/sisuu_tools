"""Commercial tables — email leads and usage logs.

Revision ID: 002_commercial
Revises: 001_initial
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002_commercial"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "email_leads",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=20), server_default="active", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_email_leads_email", "email_leads", ["email"], unique=False)

    op.create_table(
        "usage_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("visitor_id", sa.String(length=64), nullable=False),
        sa.Column("tool_slug", sa.String(length=255), nullable=False),
        sa.Column("tier", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_usage_logs_visitor_id", "usage_logs", ["visitor_id"], unique=False)
    op.create_index("ix_usage_logs_created_at", "usage_logs", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_usage_logs_created_at", table_name="usage_logs")
    op.drop_index("ix_usage_logs_visitor_id", table_name="usage_logs")
    op.drop_table("usage_logs")
    op.drop_index("ix_email_leads_email", table_name="email_leads")
    op.drop_table("email_leads")
