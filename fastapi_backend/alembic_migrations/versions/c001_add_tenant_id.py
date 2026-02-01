"""Add tenant support

Revision ID: c001_add_tenant_id
Revises: b389592974f8
Create Date: 2026-02-01 00:00:00.000000

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c001_add_tenant_id"
down_revision: Union[str, None] = "b389592974f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tenants table
    op.create_table(
        "tenants",
        sa.Column("id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), onupdate=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tenants_slug"), "tenants", ["slug"], unique=True)

    # Add tenant_id to user table
    op.add_column(
        "user",
        sa.Column("tenant_id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True)
    )

    # Create foreign key constraint
    op.create_foreign_key(
        "fk_user_tenant_id",
        "user", "tenants",
        ["tenant_id"], ["id"],
    )

    # Create default tenant
    op.execute(
        sa.insert(sa.table(
            "tenants",
            sa.column("id", fastapi_users_db_sqlalchemy.generics.GUID()),
            sa.column("name"),
            sa.column("slug"),
            sa.column("is_active"),
        )).values(
            id="00000000-0000-0000-0000-000000000001",
            name="Default Tenant",
            slug="default",
            is_active=True,
        )
    )

    # Set existing users to default tenant
    op.execute(
        sa.update(sa.table("user", sa.column("tenant_id")))
        .values(tenant_id="00000000-0000-0000-0000-000000000001")
    )

    # Make tenant_id NOT NULL after setting default values
    op.alter_column(
        "user",
        "tenant_id",
        nullable=False,
    )


def downgrade() -> None:
    # Make tenant_id nullable again
    op.alter_column(
        "user",
        "tenant_id",
        nullable=True,
    )

    # Drop foreign key
    op.drop_constraint("fk_user_tenant_id", "user", type_="foreignkey")

    # Drop tenant_id column
    op.drop_column("user", "tenant_id")

    # Drop tenants table
    op.drop_index(op.f("ix_tenants_slug"), table_name="tenants")
    op.drop_table("tenants")
