"""Enable PostgreSQL Row-Level Security for multi-tenancy

Revision ID: c003_enable_rls_policies
Revises: c002_add_tenant_id_to_items
Create Date: 2026-02-01 12:30:00.000000

This migration enables PostgreSQL Row-Level Security (RLS) on the items
and user tables to enforce tenant isolation at the database level.

Security Design:
- RLS policies use app.current_tenant configuration parameter
- If current_tenant is not set, all rows are blocked (default-deny)
- tenants table is excluded from RLS for tenant resolution
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c003_enable_rls_policies"
down_revision: Union[str, None] = "c002_add_tenant_id_to_items"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ============================================================
    # ENABLE ROW LEVEL SECURITY
    # ============================================================

    # Enable RLS on items table
    op.execute("ALTER TABLE items ENABLE ROW LEVEL SECURITY")

    # Enable RLS on user table (use quotes because "user" is a reserved keyword)
    op.execute('ALTER TABLE "user" ENABLE ROW LEVEL SECURITY')

    # ============================================================
    # CREATE RLS POLICIES
    # ============================================================

    # Create tenant isolation policy for items table
    # This policy ensures users can only see items from their tenant
    # Check if value looks like UUID before casting to avoid errors with 'admin_bypass'
    op.execute("""
        CREATE POLICY tenant_isolation_policy ON items
        FOR ALL
        USING (
            current_setting('app.current_tenant', true) ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            AND tenant_id = current_setting('app.current_tenant', true)::uuid
        )
        WITH CHECK (
            current_setting('app.current_tenant', true) ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            AND tenant_id = current_setting('app.current_tenant', true)::uuid
        )
    """)

    # Create tenant isolation policy for user table
    # This ensures users can only see other users from their tenant
    op.execute('''
        CREATE POLICY tenant_isolation_policy ON "user"
        FOR ALL
        USING (
            current_setting('app.current_tenant', true) ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            AND tenant_id = current_setting('app.current_tenant', true)::uuid
        )
        WITH CHECK (
            current_setting('app.current_tenant', true) ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
            AND tenant_id = current_setting('app.current_tenant', true)::uuid
        )
    ''') 

    # ============================================================
    # CREATE BYPASS POLICY FOR SUIT (ADMIN) CONTEXT
    # ============================================================

    # Allow admins to bypass RLS when using admin_bypass context
    # When app.current_tenant is set to 'admin_bypass', all rows are visible
    op.execute("""
        CREATE POLICY admin_bypass_policy ON items
        FOR ALL
        USING (current_setting('app.current_tenant', true) = 'admin_bypass')
        WITH CHECK (current_setting('app.current_tenant', true) = 'admin_bypass')
    """)

    op.execute('''
        CREATE POLICY admin_bypass_policy ON "user"
        FOR ALL
        USING (current_setting('app.current_tenant', true) = 'admin_bypass')
        WITH CHECK (current_setting('app.current_tenant', true) = 'admin_bypass')
    ''')

    # Note: tenants table is NOT enabled for RLS
    # This allows tenant resolution without knowing the tenant in advance


def downgrade() -> None:
    # Drop policies
    op.execute("DROP POLICY IF EXISTS admin_bypass_policy ON items")
    op.execute('DROP POLICY IF EXISTS admin_bypass_policy ON "user"')
    op.execute("DROP POLICY IF EXISTS tenant_isolation_policy ON items")
    op.execute('DROP POLICY IF EXISTS tenant_isolation_policy ON "user"')

    # Disable RLS
    op.execute("ALTER TABLE items DISABLE ROW LEVEL SECURITY")
    op.execute('ALTER TABLE "user" DISABLE ROW LEVEL SECURITY')
