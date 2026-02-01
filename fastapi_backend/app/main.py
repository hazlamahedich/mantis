from typing import Any

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.config import settings
from app.core.logging import configure_logging
from app.core.metrics import setup_metrics
from app.core.middleware import RequestLoggingMiddleware
from app.routes.auth import router as auth_router
from app.routes.health import router as health_router
from app.routes.items import router as items_router
from app.utils import simple_generate_unique_route_id

# Configure structured logging (must happen before importing logging-using modules)
configure_logging()

app = FastAPI(
    generate_unique_id_function=simple_generate_unique_route_id,
    openapi_url=settings.OPENAPI_URL,
)

# Add Prometheus instrumentation
setup_metrics(app)

# Middleware for CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware (must be after CORS)
app.add_middleware(RequestLoggingMiddleware)

# Configure OAuth2 for Swagger UI
# This allows developers to test protected routes in /docs
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
    scopes={
        "openid": "OpenID Connect scope",
        "profile": "User profile information",
        "email": "User email address",
    },
)


def get_swagger_config() -> dict[str, Any]:
    """Configure OpenAPI/Swagger with OAuth2 for Keycloak."""
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title="Mantis Bot API",
        version=settings.APP_VERSION,
        description="Multi-tenant AI chatbot platform API",
        routes=app.routes,
    )

    # Add security schemes and servers
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "Local development"}
    ]
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2AuthorizationCodeBearer": {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth",
                    "tokenUrl": f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
                    "scopes": {
                        "openid": "OpenID Connect scope",
                        "profile": "User profile information",
                        "email": "User email address",
                    },
                }
            },
        }
    }
    openapi_schema["security"] = [
        {"OAuth2AuthorizationCodeBearer": ["openid", "profile", "email"]}
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Set custom OpenAPI schema for Swagger UI
app.openapi = get_swagger_config

# Include authentication routes (Keycloak-based)
app.include_router(auth_router)

# Include items routes
app.include_router(items_router, prefix="/items")

# Include health check routes
app.include_router(health_router)

add_pagination(app)
