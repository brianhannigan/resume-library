"""init tables

Revision ID: 0001
Revises: 
Create Date: 2025-08-29

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("datetime_utc", sa.DateTime, nullable=False),
        sa.Column("company", sa.String, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("source", sa.String, nullable=True),
        sa.Column("location", sa.String, nullable=True),
        sa.Column("job_url", sa.String, nullable=True),
        sa.Column("status", sa.String, nullable=False, server_default="parsed"),
        sa.Column("salary_min", sa.Integer, nullable=True),
        sa.Column("salary_max", sa.Integer, nullable=True),
        sa.Column("contact_name", sa.String, nullable=True),
        sa.Column("contact_email", sa.String, nullable=True),
        sa.Column("profile_used", sa.String, nullable=True),
        sa.Column("resume_path", sa.String, nullable=True),
        sa.Column("cover_letter_path", sa.String, nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("error", sa.Text, nullable=True),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("application_id", sa.Integer, nullable=False),
        sa.Column("ts", sa.DateTime, nullable=False),
        sa.Column("event_type", sa.String, nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("json_blob", sa.Text, nullable=True),
    )

def downgrade():
    op.drop_table("audit_events")
    op.drop_table("applications")
