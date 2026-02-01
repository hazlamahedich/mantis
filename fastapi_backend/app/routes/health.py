"""Health check routes for infrastructure validation."""

from typing import Any

from fastapi import APIRouter
from sqlalchemy import text

from app.database import get_async_session
from app.config import settings

router = APIRouter(tags=["health"])


async def check_postgres() -> str:
    """Check PostgreSQL connectivity."""
    try:
        async for session in get_async_session():
            result = await session.execute(text("SELECT 1"))
            result.fetchone()
            return "ok"
    except Exception as e:
        return f"error: {str(e)[:50]}"


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
        return f"error: {str(e)[:50]}"


@router.get("/health")
async def health_check() -> dict[str, Any]:
    """
    Health check endpoint for infrastructure services.
    
    Returns status of PostgreSQL and Redis connectivity.
    Returns 200 if all services are healthy.
    """
    postgres_status = await check_postgres()
    redis_status = await check_redis()
    
    overall_status = "healthy"
    if postgres_status != "ok" or redis_status != "ok":
        overall_status = "unhealthy"
    
    return {
        "status": overall_status,
        "postgres": postgres_status,
        "redis": redis_status,
    }


@router.get("/health/live")
async def liveness() -> dict[str, str]:
    """Simple liveness probe for container orchestration."""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness() -> dict[str, Any]:
    """Readiness probe - only returns 200 if dependencies are ready."""
    postgres_status = await check_postgres()
    redis_status = await check_redis()
    
    if postgres_status != "ok" or redis_status != "ok":
        return {
            "status": "not_ready",
            "postgres": postgres_status,
            "redis": redis_status,
        }
    
    return {
        "status": "ready",
        "postgres": postgres_status,
        "redis": redis_status,
    }
