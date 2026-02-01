"""
Tenant middleware for extracting tenant_id from JWT and setting context.

This middleware:
1. Extracts tenant_id from JWT claims (via authenticated user)
2. Sets the tenant context variable for database RLS
3. Logs tenant context changes for security auditing
"""
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.tenant import set_tenant_id, get_tenant_id
from app.core.logging import get_logger
from app.models import User


logger = get_logger(__name__)


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract and set tenant context from JWT.

    This middleware runs after authentication to extract the tenant_id
    from the authenticated user and set it in the tenant context variable.
    This ensures all database queries are automatically scoped via RLS.

    Note: Authentication routes (login, register) are excluded via
    SudoContext since they don't have a tenant yet.
    """

    # Paths that should bypass tenant context setting
    # These routes handle login/registration where tenant isn't known yet
    BYPASS_PATHS = {
        "/auth/jwt/login",
        "/auth/register",
        "/auth/forgot-password",
        "/auth/verify",
        "/health",
        "/openapi.json",
        "/docs",
        "/redoc",
    }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and set tenant context.

        1. Check if path should bypass tenant extraction
        2. Get authenticated user from request state (set by auth)
        3. Set tenant context from user.tenant_id
        4. Log tenant context for security auditing
        5. Process request
        6. Clear tenant context after request
        """
        # Check if this path should bypass tenant context
        if self._should_bypass(request.url.path):
            return await call_next(request)

        # Try to get authenticated user from request state
        # The auth dependency sets request.state.user
        user: User | None = getattr(request.state, "user", None)

        if user and hasattr(user, "tenant_id") and user.tenant_id:
            # Set tenant context for this request
            set_tenant_id(user.tenant_id)

            logger.debug(
                "tenant_context_set",
                tenant_id=str(user.tenant_id),
                user_id=str(user.id),
                path=request.url.path,
            )
        else:
            # No tenant context - this is a security concern
            # for authenticated requests on non-bypassed paths
            logger.warning(
                "tenant_context_missing",
                path=request.url.path,
                user_id=str(user.id) if user else None,
            )

        try:
            # Process request with tenant context set
            response = await call_next(request)
            return response
        finally:
            # Clear tenant context after request completes
            # This prevents context leakage between requests
            set_tenant_id(None)

    def _should_bypass(self, path: str) -> bool:
        """
        Check if the given path should bypass tenant context.

        Args:
            path: Request URL path

        Returns:
            True if path should bypass tenant extraction
        """
        # Exact match bypass
        if path in self.BYPASS_PATHS:
            return True

        # Prefix match for docs/static assets
        for bypass in self.BYPASS_PATHS:
            if path.startswith(bypass):
                return True

        return False
