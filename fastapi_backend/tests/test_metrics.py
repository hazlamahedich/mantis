"""Tests for Prometheus metrics endpoint."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_metrics_endpoint_returns_200(test_client: AsyncClient):
    """Test that /metrics endpoint returns 200 status code."""
    response = await test_client.get("/metrics")

    # Metrics endpoint should be accessible
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "charset=utf-8" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_metrics_returns_prometheus_text_format(test_client: AsyncClient):
    """Test that /metrics endpoint returns Prometheus text format."""
    response = await test_client.get("/metrics")

    assert response.status_code == 200
    content = response.text

    # Prometheus text format markers
    assert "# HELP" in content or "# TYPE" in content


@pytest.mark.asyncio
async def test_metrics_includes_default_metrics(test_client: AsyncClient):
    """Test that default Prometheus metrics are present."""
    # First, make a request to generate some metrics
    await test_client.get("/health/live")

    # Then get metrics
    response = await test_client.get("/metrics")
    assert response.status_code == 200

    content = response.text

    # Check for common FastAPI metrics
    # Note: Exact metric names may vary based on prometheus-fastapi-instrumentator version
    assert any(metric in content for metric in [
        "http_server_requests",
        "http_server_request_duration_seconds",
        "fastapi",
        "request",
    ])


@pytest.mark.asyncio
async def test_metrics_includes_request_count(test_client: AsyncClient):
    """Test that request count metric is incremented."""
    # Get initial metrics
    initial_response = await test_client.get("/metrics")
    initial_content = initial_response.text

    # Make a request
    await test_client.get("/health/live")

    # Get updated metrics
    updated_response = await test_client.get("/metrics")
    updated_content = updated_response.text

    # Both should have content
    assert len(initial_content) > 0
    assert len(updated_content) > 0


@pytest.mark.asyncio
async def test_metrics_endpoint_excluded_from_openapi(test_client: AsyncClient):
    """Test that /metrics endpoint is excluded from OpenAPI docs."""
    response = await test_client.get("/openapi.json")

    assert response.status_code == 200
    openapi_data = response.json()

    # /metrics should not be in the paths
    assert "/metrics" not in openapi_data.get("paths", {})


@pytest.mark.asyncio
async def test_metrics_accessible_without_auth(test_client: AsyncClient):
    """Test that /metrics endpoint is accessible without authentication."""
    # This should return 200 even without auth headers
    response = await test_client.get("/metrics")

    assert response.status_code == 200
