"""Prometheus metrics configuration."""

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def setup_metrics(app: FastAPI) -> None:
    """
    Setup Prometheus metrics instrumentation.

    Exposes /metrics endpoint and instruments all handlers.
    """
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=True,
        should_group_untemplated=False,
        excluded_handlers=["/metrics"],
        env_var_name="METRICS_ENABLED",
    )
    instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
