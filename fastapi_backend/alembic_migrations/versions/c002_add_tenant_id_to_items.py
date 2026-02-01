"""Add tenant_id to items table

Revision ID: c002_add_tenant_id_to_items
Revises: c001_add_tenant_id
Create Date: 2026-02-01 12:00:00.000000

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c002_add_tenant_id_to_items"
down_revision: Union[str, None] = "c001_add_tenant_id"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add tenant_id column to items table (nullable initially)
    op.add_column(
        "items",
        sa.Column("tenant_id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True)
    )

    # Create foreign key constraint
    op.create_foreign_key(
        "fk_items_tenant_id",
        "items", "tenants",
        ["tenant_id"], ["id"],
    )

    # Set existing items to default tenant
    op.execute(
        sa.update(sa.table("items", sa.column("tenant_id")))
        .values(tenant_id="00000000-0000-0000-0000-000000000001")
    )

    # Make tenant_id NOT NULL after setting default values
    op.alter_column(
        "items",
        "tenant_id",
        nullable=False,
    )


def downgrade() -> None:
    # Make tenant_id nullable again
    op.alter_column(
        "items",
        "tenant_id",
        nullable=True,
    )

    # Drop foreign key
    op.drop_constraint("fk_items_tenant_id", "items", type_="foreignkey")

    # Drop tenant_id column
    op.drop_column("items", "tenant_id")
