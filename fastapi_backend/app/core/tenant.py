"""
Tenant context management for multi-tenancy with PostgreSQL RLS.

This module provides:
1. Async-safe tenant context storage using contextvars
2. TenantSession that sets app.current_tenant on DB connection
3. SudoContext for admin operations that bypass RLS
"""
from contextvars import ContextVar
from typing import Union, AsyncGenerator, Optional
from uuid import UUID
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


# ============================================================
# TENANT CONTEXT STORAGE
# ============================================================

# Tenant context can be:
# - UUID: Normal tenant context for queries
# - "admin_bypass": Special flag to bypass RLS for admin operations
# - None: No tenant context set (queries will return 0 rows due to RLS)
tenant_context: ContextVar[Union[UUID, str, None]] = ContextVar("tenant_context", default=None)


def get_tenant_id() -> Union[UUID, str, None]:
    """
    Get the current tenant context value.

    Returns:
        UUID of current tenant, "admin_bypass" for sudo mode, or None
    """
    return tenant_context.get()


def set_tenant_id(tenant_id: Union[UUID, str, None]) -> None:
    """
    Set the tenant context for the current async context.

    Args:
        tenant_id: UUID of tenant, "admin_bypass" for sudo, or None
    """
    tenant_context.set(tenant_id)


# ============================================================
# TENANT-AWARE DATABASE SESSION
# ============================================================

class TenantSession(AsyncSession):
    """
    AsyncSession that automatically sets tenant context on connection.

    When the session is entered, it sets the app.current_tenant PostgreSQL
    configuration parameter based on the current tenant context variable.

    This ensures all queries in the session are automatically scoped to
    the current tenant via PostgreSQL RLS policies.

    IMPORTANT: The session MUST be used as a context manager (async with)
    for the tenant context to be set properly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_tenant_id = None
        self._config_set_for_transaction = False

    async def _set_tenant_config(self):
        """Set the tenant config if it has changed."""
        current_tenant = get_tenant_id()

        # Only re-set if the tenant has changed
        if current_tenant != self._last_tenant_id:
            self._last_tenant_id = current_tenant
            self._config_set_for_transaction = False  # Reset flag when tenant changes

            # Ensure we send a string value (or empty string for None)
            # Empty string will fail regex check in RLS policy, safely returning false/blocking access
            tenant_value = str(current_tenant) if current_tenant is not None else ""

            # Use the parent class execute directly (bypassing our override)
            await super().execute(
                text("SELECT set_config('app.current_tenant', :tenant_id, false)"),
                {"tenant_id": tenant_value}
            )
            self._config_set_for_transaction = True

    async def __aenter__(self) -> AsyncSession:
        # Call parent's __aenter__ first
        session = await super().__aenter__()

        # Set initial tenant config
        await self._set_tenant_config()

        return session

    async def execute(self, statement, params=None, **kwargs):
        # Check if tenant context has changed and update config
        await self._set_tenant_config()

        # Execute the query
        return await super().execute(statement, params=params, **kwargs)


# ============================================================
# SUDO CONTEXT MANAGER
# ============================================================

@asynccontextmanager
async def sudo_context():
    """
    Context manager that bypasses RLS for admin operations.

    Usage:
        async with sudo_context():
            # This code can see all data across all tenants
            await some_admin_operation()

    This sets app.current_tenant to "admin_bypass" which is matched
    by the admin_bypass_policy RLS policy to allow all rows.
    """
    # Store the original tenant context
    token = tenant_context.set("admin_bypass")

    try:
        yield
    finally:
        # Restore the original tenant context
        tenant_context.reset(token)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

@asynccontextmanager
async def tenant_context_scope(tenant_id: Union[UUID, str]):
    """
    Context manager to temporarily set tenant context.

    Useful for background jobs or operations that need to switch tenants.

    Args:
        tenant_id: UUID of tenant to set as context

    Example:
        async with tenant_context_scope(some_tenant_id):
            # All DB operations here use this tenant
            await process_items_for_tenant()
    """
    token = tenant_context.set(tenant_id)

    try:
        yield
    finally:
        tenant_context.reset(token)


async def get_tenant_sessionmaker(sessionmaker_class, tenant_id: Union[UUID, str, None] = None) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a TenantSession with optional tenant context.

    This is a drop-in replacement for get_async_session() that
    uses TenantSession instead of regular AsyncSession.

    Args:
        sessionmaker_class: The async_sessionmaker to use
        tenant_id: Optional tenant_id to set as context

    Yields:
        TenantSession with tenant context configured
    """
    # Set tenant context if provided
    if tenant_id is not None:
        set_tenant_id(tenant_id)

    # Create session with tenant context
    async with sessionmaker_class(class_=TenantSession) as session:
        yield session
