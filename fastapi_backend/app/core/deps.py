"""
FastAPI dependency functions for authentication.

These dependencies extract JWT tokens from HTTP requests and provide
user authentication for protected routes.
"""

from typing import Annotated

from fastapi import Cookie, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user as _get_current_user
from app.core.auth import get_current_user_optional as _get_current_user_optional
from app.database import get_async_session
from app.models import User


async def get_token(
    authorization: Annotated[str | None, Header()] = None,
    auth_access_token: Annotated[str | None, Cookie()] = None,
) -> str | None:
    """
    Extract JWT token from Authorization header or Cookie.

    FastAPI dependency that extracts the Bearer token from the
    Authorization header or 'auth_access_token' cookie.

    Args:
        authorization: Value of Authorization header (auto-injected)
        auth_access_token: Value of auth_access_token cookie (auto-injected)

    Returns:
        JWT token string without "Bearer " prefix, or None if not provided
    """
    if authorization:
        if authorization.startswith("Bearer "):
            return authorization[7:]
        return authorization

    return auth_access_token


# Type alias for database session
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
# Type alias for auth token
TokenDep = Annotated[str | None, Depends(get_token)]


async def get_current_user(
    session: SessionDep,
    token: TokenDep,
) -> User:
    """
    FastAPI dependency for required authentication.

    Use this dependency in protected routes to ensure the user
    is authenticated. Raises 401 if authentication fails.

    Example:
        ```python
        @app.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"message": f"Hello, {user.email}"}
        ```
    """
    return await _get_current_user(token or "", session)


async def get_current_user_optional(
    session: SessionDep,
    token: TokenDep,
) -> User | None:
    """
    FastAPI dependency for optional authentication.

    Use this dependency in routes that work for both authenticated
    and anonymous users. Returns None if not authenticated.

    Example:
        ```python
        @app.get("/public")
        async def public_route(user: User | None = Depends(get_current_user_optional)):
            if user:
                return {"message": f"Hello, {user.email}"}
            return {"message": "Hello, anonymous"}
        ```
    """
    return await _get_current_user_optional(token, session)
