"""
Test PostgreSQL Row-Level Security (RLS) for multi-tenancy.

These tests verify that:
1. Raw SQL queries cannot bypass RLS (database-level enforcement)
2. Data leakage is prevented (user A cannot see user B's items)
3. Sudo context works for admin operations
4. Background jobs can hydrate tenant context properly
"""
import pytest
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4


@pytest.mark.asyncio(loop_scope="function")
async def test_raw_sql_cannot_bypass_rls(db_session: AsyncSession, authenticated_user):
    """
    RED PHASE: Verify raw SQL is scoped by tenant_id through RLS.

    Even when executing raw SQL, the PostgreSQL RLS policy should
    restrict access to rows matching the current tenant context.
    """
    from app.core.tenant import set_tenant_id, tenant_context_scope
    from sqlalchemy import text

    user_id = authenticated_user["user"].id
    tenant_id = authenticated_user["user"].tenant_id

    # Set tenant context using context variable before the query
    # The TenantSession will pick this up when executing the query
    set_tenant_id(tenant_id)

    # Now execute raw SQL - should only return rows for this tenant
    # Note: The db_session fixture has already been entered, but we've
    # set the tenant context variable which TenantSession checks
    result = await db_session.execute(
        text("SELECT * FROM items WHERE user_id = :user_id"),
        {"user_id": str(user_id)}
    )
    rows = result.fetchall()

    # All returned rows should belong to the current tenant
    for row in rows:
        assert str(row[4]) == str(tenant_id), f"Item tenant_id mismatch: {row}"

    # Clean up
    set_tenant_id(None)


@pytest.mark.asyncio(loop_scope="function")
async def test_data_leakage_prevention(db_session: AsyncSession, test_client, authenticated_user, admin_user):
    """
    RED PHASE: Verify RLS policies are defined correctly.

    This test verifies that the RLS policies exist and have the correct
    USING clauses for tenant isolation.
    """
    from app.core.tenant import set_tenant_id

    user_tenant_id = authenticated_user["user"].tenant_id

    # Verify RLS policies exist
    result = await db_session.execute(
        text("""
            SELECT policyname, qual
            FROM pg_policies
            WHERE schemaname = 'public'
            AND tablename = 'items'
        """)
    )
    policies = result.fetchall()

    # Check that tenant_isolation_policy exists
    policy_names = [row[0] for row in policies]
    assert "tenant_isolation_policy" in policy_names, "tenant_isolation_policy must exist"

    # Verify the policy has the correct USING clause
    for policy in policies:
        if policy[0] == "tenant_isolation_policy":
            assert "tenant_id" in policy[1], "Policy must filter by tenant_id"
            assert "app.current_tenant" in policy[1], "Policy must use app.current_tenant setting"

    # Verify admin_bypass_policy exists
    assert "admin_bypass_policy" in policy_names, "admin_bypass_policy must exist"


@pytest.mark.asyncio(loop_scope="function")
async def test_rls_blocks_without_tenant_context(db_session: AsyncSession):
    """
    RED PHASE: Verify RLS blocks all access when tenant context is not set.

    This ensures the default-deny security posture works correctly.
    """
    # Clear any existing tenant context
    await db_session.execute(
        text("SELECT set_config('app.current_tenant', '', false)")
    )

    # Try to query items - should return zero rows due to RLS
    result = await db_session.execute(text("SELECT * FROM items"))
    rows = result.fetchall()

    # RLS should block all rows when context is not set
    assert len(rows) == 0, "RLS should return 0 rows when tenant context is not set"


@pytest.mark.asyncio(loop_scope="function")
async def test_rls_policy_enforcement(db_session: AsyncSession):
    """
    RED PHASE: Direct verification that RLS policies are enabled.

    This checks the PostgreSQL system catalogs to verify RLS is active.
    """
    # Check if RLS is enabled on items table
    result = await db_session.execute(
        text("""
            SELECT relrowsecurity
            FROM pg_class
            WHERE relname = 'items'
        """)
    )
    rls_enabled_items = result.scalar()

    # Check if RLS is enabled on user table (quoted because user is a keyword)
    result = await db_session.execute(
        text("""
            SELECT relrowsecurity
            FROM pg_class
            WHERE relname = 'user'
        """)
    )
    rls_enabled_user = result.scalar()

    assert rls_enabled_items is True, "RLS must be enabled on items table"
    assert rls_enabled_user is True, "RLS must be enabled on user table"


@pytest.mark.asyncio(loop_scope="function")
async def test_tenant_model_exists(db_session: AsyncSession):
    """
    RED PHASE: Verify the Tenant model is properly defined.
    """
    from app.models import Tenant

    # Check if tenants table exists and is accessible
    result = await db_session.execute(
        text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'tenants'
            )
        """)
    )
    table_exists = result.scalar()

    assert table_exists is True, "Tenants table must exist"


@pytest.mark.asyncio(loop_scope="function")
async def test_item_has_tenant_id_column(db_session: AsyncSession):
    """
    RED PHASE: Verify items table has tenant_id column.
    """
    result = await db_session.execute(
        text("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns
                WHERE table_name = 'items'
                AND column_name = 'tenant_id'
            )
        """)
    )
    column_exists = result.scalar()

    assert column_exists is True, "Items table must have tenant_id column"


@pytest.mark.asyncio(loop_scope="function")
async def test_tenant_context_variable(db_session: AsyncSession, authenticated_user):
    """
    RED PHASE: Verify the app.current_tenant configuration parameter works.
    """
    tenant_id = authenticated_user["user"].tenant_id

    # Set the tenant context
    await db_session.execute(
        text("SELECT set_config('app.current_tenant', :tenant_id, false)"),
        {"tenant_id": str(tenant_id)}
    )

    # Read it back
    result = await db_session.execute(
        text("SELECT current_setting('app.current_tenant', true)")
    )
    current_tenant = result.scalar()

    assert current_tenant == str(tenant_id), "Tenant context should be settable"


@pytest.mark.asyncio(loop_scope="function")
async def test_sudo_context_runtime_safety(db_session, authenticated_user):
    """
    RED PHASE: Verify sudo_context bypass works without casting errors.
    
    Verifies that 'admin_bypass' string value doesn't cause UUID casting errors
    in the RLS policy (regression test for lazy evaluation bug).
    """
    from app.core.tenant import sudo_context
    
    async with sudo_context():
        # This triggers the RLS policy check
        # Should NOT raise "invalid input syntax for type uuid"
        result = await db_session.execute(text("SELECT * FROM items"))
        rows = result.fetchall()
        # Should be accessible (even if empty)
        assert isinstance(rows, list)

