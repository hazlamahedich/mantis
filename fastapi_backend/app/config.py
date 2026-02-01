from typing import Set
from urllib.parse import urlparse

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # OpenAPI docs
    OPENAPI_URL: str = "/openapi.json"

    # Database
    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None
    REDIS_URL: str = "redis://localhost:6379/0"
    EXPIRE_ON_COMMIT: bool = False

    # User
    ACCESS_SECRET_KEY: str
    RESET_PASSWORD_SECRET_KEY: str
    VERIFICATION_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600

    # Email
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: str | None = None
    MAIL_SERVER: str | None = None
    MAIL_PORT: int | None = None
    MAIL_FROM_NAME: str = "FastAPI template"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    TEMPLATE_DIR: str = "email_templates"

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # CORS
    CORS_ORIGINS: Set[str] | None = None

    # Observability & Monitoring
    KEYCLOAK_INTERNAL_URL: str = "http://keycloak:8080"
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "mantis"
    KEYCLOAK_CLIENT_ID: str = "mantis-backend"
    KEYCLOAK_CLIENT_SECRET: str = "backend-secret-change-in-prod"
    LOG_LEVEL: str = "INFO"
    APP_VERSION: str = "0.0.1"
    COMMIT_SHA: str = "dev"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if v is None:
            return {"http://localhost:3000", "http://localhost:8000"}
        if isinstance(v, str):
            return {origin.strip() for origin in v.split(",") if origin.strip()}
        return v

    @field_validator("KEYCLOAK_INTERNAL_URL", mode="before")
    @classmethod
    def validate_keycloak_url(cls, v: str) -> str:
        """Validate that KEYCLOAK_INTERNAL_URL is a properly formatted URL."""
        if not v:
            return v
        try:
            result = urlparse(v)
            if not all([result.scheme, result.netloc]):
                raise ValueError(
                    f"KEYCLOAK_INTERNAL_URL must be a valid URL with scheme and netloc, got: {v}"
                )
            if result.scheme not in ("http", "https"):
                raise ValueError(
                    f"KEYCLOAK_INTERNAL_URL must use http or https scheme, got: {result.scheme}"
                )
        except ValueError as e:
            raise ValueError(f"Invalid KEYCLOAK_INTERNAL_URL format: {e}")
        return v

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate LOG_LEVEL is a valid Python logging level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(
                f"LOG_LEVEL must be one of {', '.join(valid_levels)}, got: {v}"
            )
        return v_upper

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
