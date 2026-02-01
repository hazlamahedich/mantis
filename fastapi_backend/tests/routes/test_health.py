"""Tests for health check endpoints."""

import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_returns_200_when_all_services_healthy(test_client: AsyncClient):
    """Test health endpoint returns 200 when all services are healthy."""
    with patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="ok"):
        response = await test_client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "status" in data
        assert "postgres" in data
        assert "redis" in data
        assert "keycloak" in data
        assert "version" in data

        # Check all services are healthy
        assert data["postgres"] == "ok"
        assert data["redis"] == "ok"
        assert data["keycloak"] == "ok"
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_endpoint_returns_503_when_postgres_unhealthy(test_client: AsyncClient):
    """Test health endpoint returns 503 when PostgreSQL is unhealthy."""
    with patch("app.routes.health.check_postgres", new_callable=AsyncMock, return_value="error: connection failed"), \
         patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="ok"):
        response = await test_client.get("/health")

        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert "error" in data["postgres"]


@pytest.mark.asyncio
async def test_health_endpoint_returns_503_when_redis_unhealthy(test_client: AsyncClient):
    """Test health endpoint returns 503 when Redis is unhealthy."""
    with patch("app.routes.health.check_redis", new_callable=AsyncMock, return_value="error: connection refused"), \
         patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="ok"):
        response = await test_client.get("/health")

        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert "error" in data["redis"]


@pytest.mark.asyncio
async def test_health_endpoint_returns_503_when_keycloak_unhealthy(test_client: AsyncClient):
    """Test health endpoint returns 503 when Keycloak is unhealthy."""
    with patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="error: timeout"):
        response = await test_client.get("/health")

        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert "error" in data["keycloak"]


@pytest.mark.asyncio
async def test_health_endpoint_returns_503_when_multiple_services_unhealthy(test_client: AsyncClient):
    """Test health endpoint returns 503 when multiple services are unhealthy."""
    with patch("app.routes.health.check_postgres", new_callable=AsyncMock, return_value="error: db down"), \
         patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="error: auth down"):
        response = await test_client.get("/health")

        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"


@pytest.mark.asyncio
async def test_health_endpoint_includes_version_information(test_client: AsyncClient):
    """Test health endpoint includes version information."""
    with patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="ok"):
        response = await test_client.get("/health")

        assert response.status_code == 200
        data = response.json()

        # Check version information
        assert "version" in data
        assert "app_version" in data["version"]
        assert "commit_sha" in data["version"]


@pytest.mark.asyncio
async def test_readiness_endpoint_includes_keycloak(test_client: AsyncClient):
    """Test readiness endpoint includes Keycloak status."""
    with patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="ok"):
        response = await test_client.get("/health/ready")

        assert response.status_code == 200
        data = response.json()

        # Check all services are included
        assert "postgres" in data
        assert "redis" in data
        assert "keycloak" in data


@pytest.mark.asyncio
async def test_readiness_returns_503_when_unhealthy(test_client: AsyncClient):
    """Test readiness endpoint returns 503 when services are unhealthy."""
    with patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="error: down"):
        response = await test_client.get("/health/ready")

        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not_ready"


@pytest.mark.asyncio
async def test_liveness_endpoint(test_client: AsyncClient):
    """Test liveness endpoint returns 200."""
    response = await test_client.get("/health/live")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


@pytest.mark.asyncio
async def test_keycloak_health_check_success(test_client: AsyncClient):
    """Test Keycloak health check succeeds when service is up."""
    with patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="ok"):
        response = await test_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["keycloak"] == "ok"


@pytest.mark.asyncio
async def test_keycloak_health_check_failure(test_client: AsyncClient):
    """Test Keycloak health check fails when service is down."""
    with patch("app.routes.health.check_keycloak", new_callable=AsyncMock, return_value="error: connection refused"):
        response = await test_client.get("/health")

        assert response.status_code == 503
        data = response.json()
        assert "error" in data["keycloak"]
