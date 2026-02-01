"""Tests for structured logging middleware and configuration."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_request_id_added_to_response_headers(test_client: AsyncClient):
    """Test that request ID is added to response headers."""
    response = await test_client.get("/health/live")

    assert response.status_code == 200
    # Request ID should be in response headers
    assert "X-Request-ID" in response.headers
    # Should be a valid UUID format (or generated ID)
    assert len(response.headers["X-Request-ID"]) > 0


@pytest.mark.asyncio
async def test_custom_request_id_preserved_in_headers(test_client: AsyncClient):
    """Test that custom request ID from headers is preserved."""
    custom_id = "my-custom-request-id-456"
    response = await test_client.get(
        "/health/live",
        headers={"X-Request-ID": custom_id}
    )

    assert response.status_code == 200
    # The custom ID should be returned in response headers
    assert response.headers["X-Request-ID"] == custom_id


@pytest.mark.asyncio
async def test_request_id_generated_when_not_provided(test_client: AsyncClient):
    """Test that a request ID is generated when not provided in headers."""
    response = await test_client.get("/health/live")

    assert response.status_code == 200
    # A request ID should be generated and added to headers
    request_id = response.headers.get("X-Request-ID")
    assert request_id is not None
    assert len(request_id) > 0


@pytest.mark.asyncio
async def test_middleware_processes_all_requests(test_client: AsyncClient):
    """Test that middleware processes requests and doesn't break them."""
    # Test multiple endpoints to ensure middleware doesn't interfere
    endpoints = [
        "/health/live",
        "/health/ready",
    ]

    for endpoint in endpoints:
        response = await test_client.get(endpoint)
        # Should succeed without errors
        assert response.status_code in [200, 503]  # 503 if services unhealthy
        # Should have request ID header
        assert "X-Request-ID" in response.headers


@pytest.mark.asyncio
async def test_logging_configured_at_startup():
    """Test that logging configuration is callable and doesn't error."""
    from app.core.logging import configure_logging, get_logger

    # These should not raise exceptions
    configure_logging()
    logger = get_logger("test_logger")
    assert logger is not None


@pytest.mark.asyncio
async def test_logger_creates_structlog_instance():
    """Test that get_logger returns a structlog logger."""
    from app.core.logging import get_logger

    logger = get_logger("test")
    # Structlog bound logger should have info method
    assert hasattr(logger, "info")
    assert hasattr(logger, "error")
    assert hasattr(logger, "warning")


@pytest.mark.asyncio
async def test_middleware_is_registered():
    """Test that RequestLoggingMiddleware is registered in the app."""
    from app.main import app
    from app.core.middleware import RequestLoggingMiddleware

    # Check that middleware is in the app's middleware stack
    # user_middleware contains Middleware objects, check the .cls attribute
    middleware_classes = [m.cls for m in app.user_middleware]

    # At least one middleware should be our logging middleware
    assert RequestLoggingMiddleware in middleware_classes
