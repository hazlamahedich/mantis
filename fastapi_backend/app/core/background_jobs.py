"""
Background job utilities for multi-tenant ARQ jobs.

This module provides utilities for background jobs (ARQ) to properly
hydrate and manage tenant context:

1. extract_tenant_from_job(): Extract tenant_id from job metadata
2. tenant_job_context(): Context manager to set tenant for job execution
3. with_tenant_context(): Decorator to auto-hydrate tenant for job functions

Usage:
    # As a decorator on job functions
    @with_tenant_context
    async def send_daily_email(ctx: JobContext):
        # tenant_id is automatically set from job metadata
        # All DB queries here are scoped to the correct tenant
        pass

    # Or manually for more control
    async def process_items(ctx: JobContext):
        tenant_id = extract_tenant_from_job(ctx)
        async with tenant_job_context(tenant_id):
            # Process items for this tenant
            pass
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable, Optional, Union
from uuid import UUID
from functools import wraps

from .tenant import set_tenant_id, get_tenant_id, tenant_context


# ============================================================
# JOB METADATA EXTRACTION
# ============================================================

def extract_tenant_from_job(ctx: dict) -> Optional[UUID]:
    """
    Extract tenant_id from ARQ job context/metadata.

    ARQ jobs can include tenant_id in their job metadata:
    {
        'job_id': '...',
        'tenant_id': 'uuid-string',  # <- Extract this
        'user_id': 'uuid-string',
        'other': 'metadata'
    }

    Args:
        ctx: ARQ job context dictionary

    Returns:
        UUID of tenant, or None if not found in metadata

    Example:
        job = await asyncio.Queue.get()
        tenant_id = extract_tenant_from_job(job.ctx)
        if tenant_id:
            await process_for_tenant(tenant_id)
    """
    if not isinstance(ctx, dict):
        return None

    # Try different possible keys where tenant_id might be stored
    tenant_id_str = ctx.get("tenant_id")

    if not tenant_id_str:
        # Check nested metadata
        metadata = ctx.get("metadata", {})
        if isinstance(metadata, dict):
            tenant_id_str = metadata.get("tenant_id")

    if not tenant_id_str:
        return None

    # Convert string UUID to UUID object
    try:
        return UUID(tenant_id_str)
    except (ValueError, TypeError):
        return None


# ============================================================
# TENANT CONTEXT FOR JOBS
# ============================================================

@asynccontextmanager
async def tenant_job_context(tenant_id: Union[UUID, str, None]):
    """
    Context manager to set tenant context for background job execution.

    This sets the tenant context variable for the duration of the job,
    ensuring all database operations are properly scoped to the tenant.

    Args:
        tenant_id: UUID of tenant to set as context (or None for no context)

    Example:
        async def process_user_data_job(ctx: dict):
            tenant_id = extract_tenant_from_job(ctx)
            async with tenant_job_context(tenant_id):
                # All DB operations here use this tenant
                await process_user_data()
    """
    # Store original context
    original_token = tenant_context.set(tenant_id)

    try:
        yield
    finally:
        # Restore original context
        tenant_context.reset(original_token)


@asynccontextmanager
async def sudo_job_context():
    """
    Context manager for admin background jobs that bypass RLS.

    Use this for jobs that need to access data across all tenants,
    such as:
    - Aggregate reporting
    - Cross-tenant data migrations
    - System maintenance tasks

    Example:
        async def generate_daily_report(ctx: dict):
            async with sudo_job_context():
                # This job can see ALL data across ALL tenants
                await generate_cross_tenant_report()
    """
    # Set admin bypass context
    original_token = tenant_context.set("admin_bypass")

    try:
        yield
    finally:
        # Restore original context
        tenant_context.reset(original_token)


# ============================================================
# DECORATORS FOR AUTO-HYDRATION
# ============================================================

def with_tenant_context(func: Callable) -> Callable:
    """
    Decorator to automatically hydrate tenant context from job metadata.

    This decorator extracts tenant_id from the job context (first argument)
    and sets it as the tenant context for the duration of the function.

    The job function's first argument should be the ARQ job context dict.

    Args:
        func: Async job function to decorate

    Returns:
        Wrapped function with automatic tenant context hydration

    Example:
        @with_tenant_context
        async def send_daily_notification(ctx: dict):
            # tenant_id automatically set from ctx['tenant_id']
            # All DB operations here are scoped to correct tenant
            await send_notifications()

    Raises:
        No exceptions - runs function without tenant if not found in metadata
    """
    @wraps(func)
    async def wrapper(ctx: dict, *args, **kwargs):
        # Extract tenant_id from job context
        tenant_id = extract_tenant_from_job(ctx)

        # Execute with tenant context
        async with tenant_job_context(tenant_id):
            return await func(ctx, *args, **kwargs)

    return wrapper


def with_sudo_context(func: Callable) -> Callable:
    """
    Decorator to run job with admin bypass (sudo) context.

    This decorator sets the tenant context to "admin_bypass" for the
    duration of the function, allowing it to access data across all tenants.

    Use this only for jobs that legitimately need cross-tenant access.

    Args:
        func: Async job function to decorate

    Returns:
        Wrapped function with admin bypass context

    Example:
        @with_sudo_context
        async def cleanup_expired_data(ctx: dict):
            # This job can see and modify ALL data
            await cleanup_all_tenants()
    """
    @wraps(func)
    async def wrapper(ctx: dict, *args, **kwargs):
        # Execute with admin bypass context
        async with sudo_job_context():
            return await func(ctx, *args, **kwargs)

    return wrapper


# ============================================================
# HELPER FUNCTIONS
# ============================================================

async def create_job_with_tenant(
    job_queue,
    job_name: str,
    tenant_id: Union[UUID, str],
    **kwargs
) -> str:
    """
    Enqueue a job with tenant_id in metadata.

    This helper ensures tenant_id is properly included in job metadata
    so that the @with_tenant_context decorator can extract it.

    Args:
        job_queue: ARQ job queue
        job_name: Name of the job function to execute
        tenant_id: UUID of tenant for this job
        **kwargs: Additional job arguments

    Returns:
        Job ID (str)

    Example:
        job_id = await create_job_with_tenant(
            job_queue,
            'send_daily_email',
            tenant_id=user.tenant_id,
            user_id=user.id
        )
    """
    job_metadata = {
        'tenant_id': str(tenant_id),
        **kwargs
    }

    # ARQ's enqueue_job signature: job_name, *args, **kwargs
    # We pass tenant_id in kwargs as metadata
    job_id = await job_queue.enqueue_job(job_name, **job_metadata)

    return job_id
