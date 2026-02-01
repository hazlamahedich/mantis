"""Health check routes for infrastructure validation."""

import os
import httpx
import json
import logging

from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.database import get_async_session
from app.config import settings

router = APIRouter(tags=["health"])

# Version information
APP_VERSION = os.getenv("APP_VERSION", "0.0.1")
COMMIT_SHA = os.getenv("COMMIT_SHA", "dev")

# Configure logger for health check failures
logger = logging.getLogger(__name__)

# Maximum error message length for health check responses
MAX_ERROR_LENGTH = 200


async def check_postgres() -> str:
    """Check PostgreSQL connectivity."""
    try:
        async for session in get_async_session():
            result = await session.execute(text("SELECT 1"))
            result.fetchone()
            return "ok"
    except Exception as e:
        error_msg = f"error: {str(e)}"
        logger.warning(f"PostgreSQL health check failed: {error_msg}")
        return error_msg[:MAX_ERROR_LENGTH]


async def check_redis() -> str:
    """Check Redis connectivity using connection pool."""
    try:
        from redis.asyncio import Redis

        # Redis client manages its own connection pool internally
        client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        try:
            await client.ping()
            return "ok"
        finally:
            await client.aclose()
    except Exception as e:
        error_msg = f"error: {str(e)}"
        logger.warning(f"Redis health check failed: {error_msg}")
        return error_msg[:MAX_ERROR_LENGTH]


async def check_keycloak() -> str:
    """Check Keycloak connectivity via root endpoint redirect."""
    try:
        keycloak_url = getattr(settings, "KEYCLOAK_INTERNAL_URL", "http://keycloak:8080")
        # Use root endpoint which should redirect to /admin/ if Keycloak is healthy
        check_url = f"{keycloak_url.rstrip('/')}/"

        async with httpx.AsyncClient(timeout=5.0, follow_redirects=False) as client:
            response = await client.get(check_url)
            # Keycloak returns 302 redirect to /admin/ when healthy
            if response.status_code in (200, 302, 301):
                return "ok"
            else:
                return f"error: http_{response.status_code}"
    except Exception as e:
        error_msg = f"error: {str(e)}"
        logger.warning(f"Keycloak health check failed: {error_msg}")
        return error_msg[:MAX_ERROR_LENGTH]


@router.get("/health", response_model=None)
async def health_check() -> Response:
    """
    Health check endpoint for infrastructure services.

    Returns status of PostgreSQL, Redis, and Keycloak connectivity.
    Returns 200 if all services are healthy, 503 otherwise.
    """
    postgres_status = await check_postgres()
    redis_status = await check_redis()
    keycloak_status = await check_keycloak()

    # Determine overall health status
    all_healthy = (
        postgres_status == "ok" and
        redis_status == "ok" and
        keycloak_status == "ok"
    )

    overall_status = "healthy" if all_healthy else "unhealthy"

    response_data = {
        "status": overall_status,
        "postgres": postgres_status,
        "redis": redis_status,
        "keycloak": keycloak_status,
        "version": {
            "app_version": APP_VERSION,
            "commit_sha": COMMIT_SHA,
        },
    }

    http_status = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    return Response(
        content=json.dumps(response_data),
        status_code=http_status,
        media_type="application/json"
    )


@router.get("/health/live")
async def liveness() -> dict[str, str]:
    """Simple liveness probe for container orchestration."""
    return {"status": "alive"}


@router.get("/health/ready", response_model=None)
async def readiness() -> Response:
    """Readiness probe - only returns 200 if dependencies are ready."""
    postgres_status = await check_postgres()
    redis_status = await check_redis()
    keycloak_status = await check_keycloak()

    all_ready = (
        postgres_status == "ok" and
        redis_status == "ok" and
        keycloak_status == "ok"
    )

    if not all_ready:
        response_data = {
            "status": "not_ready",
            "postgres": postgres_status,
            "redis": redis_status,
            "keycloak": keycloak_status,
        }
        return Response(
            content=json.dumps(response_data),
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            media_type="application/json"
        )

    response_data = {
        "status": "ready",
        "postgres": postgres_status,
        "redis": redis_status,
        "keycloak": keycloak_status,
    }
    return Response(
        content=json.dumps(response_data),
        status_code=status.HTTP_200_OK,
        media_type="application/json"
    )
