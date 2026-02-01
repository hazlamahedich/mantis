"""
Keycloak JWT authentication module.

This module replaces fastapi-users JWT auth with Keycloak OIDC token validation.

Key Features:
- JWKS caching for 15 minutes
- Token validation using Keycloak public keys
- User synchronization with local database
- tenant_id extraction from JWT claims
"""

import time
from typing import Any

import httpx
from jose import JWTError, jwk, jwt
from jose.exceptions import ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_async_session
from app.models import User


class KeycloakJWTAuth:
    """
    Keycloak JWT token validator with JWKS caching.

    Fetches and caches JWKS (JSON Web Key Set) from Keycloak for efficient
    token signature verification without storing public keys locally.
    """

    def __init__(
        self,
        keycloak_url: str,
        realm: str,
        audience: str = "mantis-frontend",
        cache_ttl_seconds: int = 900,  # 15 minutes
    ):
        """
        Initialize Keycloak JWT authenticator.

        Args:
            keycloak_url: Base URL of Keycloak server
            realm: Keycloak realm name
            audience: Expected audience claim in tokens
            cache_ttl_seconds: JWKS cache time-to-live in seconds
        """
        self.jwks_uri = f"{keycloak_url}/realms/{realm}/protocol/openid-connect/certs"
        self.issuer = f"{keycloak_url}/realms/{realm}"
        self.audience = audience
        self._cache_ttl = cache_ttl_seconds
        self._jwks_cache: dict[str, Any] | None = None
        self._cache_timestamp: float = 0

    async def get_jwks(self) -> dict[str, Any]:
        """
        Fetch JWKS from Keycloak with caching.

        Returns JWKS from cache if fresh, otherwise fetches from Keycloak.
        Cache expires after cache_ttl_seconds (default: 15 minutes).

        Returns:
            JWKS dictionary containing keys for token verification

        Raises:
            httpx.HTTPError: If JWKS fetch fails
        """
        current_time = time.time()

        # Return cached JWKS if still fresh
        if self._jwks_cache and (current_time - self._cache_timestamp) < self._cache_ttl:
            return self._jwks_cache

        # Fetch fresh JWKS from Keycloak
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.jwks_uri)
            response.raise_for_status()
            self._jwks_cache = response.json()
            self._cache_timestamp = current_time

        # Assert non-None for mypy (we just assigned it)
        assert self._jwks_cache is not None
        return self._jwks_cache

    async def decode_token(self, token: str) -> dict[str, Any]:
        """
        Decode and validate JWT token using Keycloak JWKS.

        Args:
            token: JWT access token from Keycloak

        Returns:
            Decoded token claims as dictionary

        Raises:
            JWTError: If token is invalid, expired, or signature verification fails
            ValueError: If required claims (tenant_id) are missing
        """
        jwks = await self.get_jwks()

        # Build key list for jose library
        keys = {key["kid"]: jwk.construct(key) for key in jwks["keys"]}

        try:
            # Decode and verify token
            payload: dict[str, Any] = jwt.decode(
                token,
                keys,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
            )
        except ExpiredSignatureError:
            raise JWTError("Token has expired") from None
        except JWTError as e:
            raise JWTError(f"Invalid token: {str(e)}") from None

        # Validate required custom claims
        if "tenant_id" not in payload:
            raise ValueError("Token missing required claim: tenant_id")

        return payload


# Global KeycloakJWTAuth instance
_keycloak_auth = KeycloakJWTAuth(
    keycloak_url=settings.KEYCLOAK_INTERNAL_URL,
    realm=settings.KEYCLOAK_REALM,
    audience="mantis-frontend",
)


async def verify_token(token: str) -> dict[str, Any]:
    """
    Verify a Keycloak JWT token.

    Convenience function that uses the global KeycloakJWTAuth instance.

    Args:
        token: JWT access token from Keycloak

    Returns:
        Decoded token claims as dictionary

    Raises:
        JWTError: If token is invalid or verification fails
        ValueError: If required claims are missing
    """
    return await _keycloak_auth.decode_token(token)


async def sync_user_to_database(
    session: AsyncSession,
    user_id: str,
    email: str,
    tenant_id: str | None = None,
) -> User:
    """
    Synchronize user from Keycloak token to local database.

    Implements upsert logic: creates new user if not exists,
    updates existing user if email has changed.

    Args:
        session: SQLAlchemy async session
        user_id: UUID from Keycloak token
        email: User email from token
        tenant_id: Optional tenant_id claim (for future multi-tenancy)

    Returns:
        User instance from database
    """
    # Try to find existing user
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user:
        # Update existing user if email changed
        if user.email != email:
            user.email = email
            await session.commit()
            await session.refresh(user)
    else:
        # Create new user
        user = User(
            id=user_id,
            email=email,
            is_active=True,
            is_verified=True,  # Keycloak handles verification
            is_superuser=False,  # Superuser status managed separately
            hashed_password="",  # No longer used, but required by fastapi-users base model
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def get_current_user_optional(
    token: str | None = None,
    session: AsyncSession | None = None,
) -> User | None:
    """
    Get current user from JWT token (optional).

    Returns None if no token provided or token is invalid.
    Useful for routes that work for both authenticated and anonymous users.

    Args:
        token: JWT access token from Authorization header (optional)
        session: Optional SQLAlchemy async session (will create if not provided)

    Returns:
        User instance or None if not authenticated
    """
    if not token:
        return None

    try:
        # Remove "Bearer " prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        # Verify token and extract claims
        claims = await verify_token(token)

        # Use provided session or create new one
        if session is None:
            # Create new session for this request
            from app.database import async_session_maker

            async with async_session_maker() as new_session:
                user = await sync_user_to_database(
                    session=new_session,
                    user_id=claims["sub"],
                    email=claims.get("email", ""),
                    tenant_id=claims.get("tenant_id"),
                )
                return user
        else:
            user = await sync_user_to_database(
                session=session,
                user_id=claims["sub"],
                email=claims.get("email", ""),
                tenant_id=claims.get("tenant_id"),
            )
            return user

    except (JWTError, ValueError, httpx.HTTPError):
        # Token invalid or user sync failed - treat as not authenticated
        return None


async def get_current_user(
    token: str,
    session: AsyncSession,
) -> User:
    """
    Get current user from JWT token (required).

    FastAPI dependency function for protected routes.
    Raises 401 if no token provided or token is invalid.

    Args:
        token: JWT access token from Authorization header
        session: SQLAlchemy async session

    Returns:
        User instance

    Raises:
        HTTPException 401: If authentication fails
    """
    from fastapi import HTTPException, status
    from app.core.logging import get_logger

    logger = get_logger(__name__)

    user = await get_current_user_optional(token, session)

    if user is None:
        logger.warning("Authentication failed: Invalid or missing token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.debug("User authenticated successfully", user_id=str(user.id))
    return user
