"""
Authentication routes for Keycloak integration.

These endpoints handle token refresh and provide auth-related utilities.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.deps import SessionDep, get_current_user
from app.core.logging import get_logger
from app.models import User

logger = get_logger(__name__)


router = APIRouter(prefix="/auth", tags=["auth"])


# Response models
class TokenResponse(BaseModel):
    """Response model for token endpoints."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int


class UserInfoResponse(BaseModel):
    """Response model for user info."""

    id: str
    email: str
    is_active: bool
    is_verified: bool
    is_superuser: bool


@router.get("/me", response_model=UserInfoResponse)
async def get_user_info(
    current_user: User = Depends(get_current_user),
) -> UserInfoResponse:
    """
    Get current user information.

    Returns the authenticated user's details from the JWT token.
    """
    logger.info(
        "User info retrieved",
        user_id=str(current_user.id),
        email=current_user.email,
        is_active=current_user.is_active,
    )

    return UserInfoResponse(
        id=str(current_user.id),
        email=current_user.email,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        is_superuser=current_user.is_superuser,
    )


@router.post("/refresh")
async def refresh_token(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
) -> TokenResponse:
    """
    Refresh access token.

    Note: In a production Keycloak setup, token refresh is typically
    handled by the frontend using the refresh_token grant directly
    with Keycloak. This endpoint serves as a proxy for convenience.

    For now, this returns a placeholder response. The actual refresh
    flow should be implemented by the frontend calling Keycloak directly.
    """
    logger.info(
        "Token refresh requested",
        user_id=str(current_user.id),
        email=current_user.email,
    )

    # TODO: Implement actual token refresh with Keycloak
    # For now, return a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh should be handled by frontend directly with Keycloak",
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """
    Logout endpoint.

    Note: In a Keycloak setup, logout is typically handled by
    redirecting the user to Keycloak's logout endpoint.
    This endpoint serves as a notification hook.

    Frontend should redirect to:
    {KEYCLOAK_URL}/realms/{realm}/protocol/openid-connect/logout?
        redirect_uri={frontend_url}
    """
    from app.config import settings

    logout_url = (
        f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"
        f"/protocol/openid-connect/logout?redirect_uri={settings.FRONTEND_URL}"
    )

    logger.info(
        "User logout",
        user_id=str(current_user.id),
        email=current_user.email,
        keycloak_logout_url=logout_url,
    )

    return {
        "message": "Logout successful",
        "keycloak_logout_url": logout_url,
    }


@router.get("/verify")
async def verify_token(
    current_user: User = Depends(get_current_user),
) -> UserInfoResponse:
    """
    Verify that the current token is valid.

    Returns user information if token is valid.
    """
    logger.info(
        "Token verified",
        user_id=str(current_user.id),
        email=current_user.email,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
    )

    return UserInfoResponse(
        id=str(current_user.id),
        email=current_user.email,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        is_superuser=current_user.is_superuser,
    )


@router.post("/login")
async def login_page_info() -> dict[str, str]:
    """
    Get login page information for frontend.

    Returns the Keycloak login URL and configuration for the frontend
    to initiate the OAuth flow.
    """
    from app.config import settings

    login_url = (
        f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"
        f"/protocol/openid-connect/auth?client_id=mantis-frontend"
        f"&response_type=code&scope=openid profile email"
        f"&redirect_uri={settings.FRONTEND_URL}/auth/callback"
    )

    logger.info("Login page info requested", login_url=login_url)

    return {
        "login_url": login_url,
        "keycloak_url": settings.KEYCLOAK_URL,
        "realm": settings.KEYCLOAK_REALM,
        "client_id": "mantis-frontend",
    }
