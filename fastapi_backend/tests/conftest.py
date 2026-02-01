from httpx import AsyncClient, ASGITransport
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Generator

from app.config import settings
from app.models import User, Base
from jose import jwt

from app.database import get_async_session
from app.main import app


# Test secret for generating mock JWT tokens
_TEST_JWT_SECRET = "test-secret-for-jwt-tokens"


@pytest_asyncio.fixture(scope="function")
async def engine():
    """Create a fresh test database engine for each test function."""
    from sqlalchemy import text

    engine = create_async_engine(settings.TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # Enable RLS on tables after creation
        def enable_rls(connection):
            connection.execute(text('ALTER TABLE items ENABLE ROW LEVEL SECURITY'))
            connection.execute(text('ALTER TABLE "user" ENABLE ROW LEVEL SECURITY'))

            # Create RLS policies
            connection.execute(text("""
                CREATE POLICY tenant_isolation_policy ON items
                FOR ALL
                USING (
                    current_setting('app.current_tenant', true) ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
                    AND tenant_id = current_setting('app.current_tenant', true)::uuid
                )
                WITH CHECK (
                    current_setting('app.current_tenant', true) ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
                    AND tenant_id = current_setting('app.current_tenant', true)::uuid
                )
            """))
            connection.execute(text('''
                CREATE POLICY tenant_isolation_policy ON "user"
                FOR ALL
                USING (
                    current_setting('app.current_tenant', true) ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
                    AND tenant_id = current_setting('app.current_tenant', true)::uuid
                )
                WITH CHECK (
                    current_setting('app.current_tenant', true) ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
                    AND tenant_id = current_setting('app.current_tenant', true)::uuid
                )
            '''))
            connection.execute(text("""
                CREATE POLICY admin_bypass_policy ON items
                FOR ALL
                USING (current_setting('app.current_tenant', true) = 'admin_bypass')
                WITH CHECK (current_setting('app.current_tenant', true) = 'admin_bypass')
            """))
            connection.execute(text('''
                CREATE POLICY admin_bypass_policy ON "user"
                FOR ALL
                USING (current_setting('app.current_tenant', true) = 'admin_bypass')
                WITH CHECK (current_setting('app.current_tenant', true) = 'admin_bypass')
            '''))

        await conn.run_sync(enable_rls)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(engine):
    """Create a fresh database session for each test."""
    from app.core.tenant import TenantSession

    async_session_maker = async_sessionmaker(
        bind=engine, class_=TenantSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def test_client(db_session):
    """Fixture to create a test client that uses the test database session."""

    # General database override (raw session access)
    async def override_get_async_session():
        try:
            yield db_session
        finally:
            await db_session.close()

    # Set up test database override
    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as client:
        yield client


@pytest.fixture(scope="function")
def mock_auth():
    """
    Mock Keycloak authentication for testing.

    This fixture patches the KeycloakJWTAuth to accept test tokens
    signed with the test secret.
    """
    from app.core import auth as auth_module

    # Store original methods
    original_decode_token = auth_module.KeycloakJWTAuth.decode_token
    original_verify_token = auth_module.verify_token
    original_get_current_user_optional = auth_module.get_current_user_optional

    # Create mock functions
    async def mock_decode_token(self, token: str):
        """Mock decode that accepts HS256 test tokens."""
        try:
            payload = jwt.decode(
                token,
                _TEST_JWT_SECRET,
                algorithms=["HS256"],
                audience="mantis-frontend",
                issuer=f"{settings.KEYCLOAK_INTERNAL_URL}/realms/{settings.KEYCLOAK_REALM}",
            )
            return payload
        except Exception as e:
            raise

    async def mock_verify_token(token: str):
        """Mock verify that accepts HS256 test tokens."""
        payload = jwt.decode(
            token,
            _TEST_JWT_SECRET,
            algorithms=["HS256"],
            audience="mantis-frontend",
            issuer=f"{settings.KEYCLOAK_INTERNAL_URL}/realms/{settings.KEYCLOAK_REALM}",
        )
        return payload

    # Apply patches
    with patch.object(
        auth_module.KeycloakJWTAuth, "decode_token", mock_decode_token
    ), patch.object(auth_module, "verify_token", mock_verify_token):
        yield
        # Patches are automatically undone after context exit


@pytest_asyncio.fixture(scope="function")
async def authenticated_user(test_client, db_session, mock_auth):
    """
    Fixture to create and authenticate a test user.

    This fixture creates a user in the database and returns a mock
    JWT token that can be used for authentication in tests.
    """
    from uuid import uuid4
    import time
    from app.models import Tenant

    # Create a test tenant first
    tenant_id = uuid4()
    tenant = Tenant(
        id=tenant_id,
        name="Test Tenant",
        slug="test-tenant",
    )
    db_session.add(tenant)
    await db_session.commit()

    # Create a test user directly in the database
    user_id = uuid4()
    user = User(
        id=user_id,
        email="test@example.com",
        is_active=True,
        is_superuser=False,
        is_verified=True,
        hashed_password="test",
        tenant_id=tenant_id,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Create a mock JWT token
    payload = {
        "sub": str(user_id),
        "email": "test@example.com",
        "email_verified": True,
        "tenant_id": "test-tenant-123",
        "iss": f"{settings.KEYCLOAK_INTERNAL_URL}/realms/{settings.KEYCLOAK_REALM}",
        "aud": "mantis-frontend",
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
    }

    mock_token = jwt.encode(payload, _TEST_JWT_SECRET, algorithm="HS256")

    return {
        "headers": {"Authorization": f"Bearer {mock_token}"},
        "user": user,
        "token": mock_token,
    }


@pytest_asyncio.fixture(scope="function")
async def admin_user(test_client, db_session, mock_auth):
    """
    Fixture to create an admin user for testing.
    """
    from uuid import uuid4
    import time
    from app.models import Tenant

    # Create a test tenant first
    tenant_id = uuid4()
    tenant = Tenant(
        id=tenant_id,
        name="Admin Tenant",
        slug="admin-tenant",
    )
    db_session.add(tenant)
    await db_session.commit()

    # Create an admin user directly in the database
    user_id = uuid4()
    user = User(
        id=user_id,
        email="admin@example.com",
        is_active=True,
        is_superuser=True,
        is_verified=True,
        hashed_password="admin",
        tenant_id=tenant_id,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Create a mock JWT token
    payload = {
        "sub": str(user_id),
        "email": "admin@example.com",
        "email_verified": True,
        "tenant_id": "test-tenant-123",
        "iss": f"{settings.KEYCLOAK_INTERNAL_URL}/realms/{settings.KEYCLOAK_REALM}",
        "aud": "mantis-frontend",
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()),
    }

    mock_token = jwt.encode(payload, _TEST_JWT_SECRET, algorithm="HS256")

    return {
        "headers": {"Authorization": f"Bearer {mock_token}"},
        "user": user,
        "token": mock_token,
    }
