"""Test that async factory works correctly."""
import pytest
from tests.factories.user_factory import create_user_factory


@pytest.mark.asyncio
async def test_user_factory_creates_valid_user(db_session):
    """Test that UserFactory creates a valid user with all required fields."""
    factory = await create_user_factory(db_session)
    user = await factory.create()

    assert user.id is not None
    assert user.email is not None
    assert user.hashed_password is not None
    assert user.is_active is True
    assert user.is_superuser is False
    assert user.is_verified is True


@pytest.mark.asyncio
async def test_user_factory_with_custom_attributes(db_session):
    """Test that UserFactory accepts custom attributes."""
    factory = await create_user_factory(db_session)
    user = await factory.create(
        email="custom@example.com",
        is_superuser=True,
        is_active=False,
    )

    assert user.email == "custom@example.com"
    assert user.is_superuser is True
    assert user.is_active is False


@pytest.mark.asyncio
async def test_user_factory_creates_unique_users(db_session):
    """Test that UserFactory creates unique users."""
    factory = await create_user_factory(db_session)
    user1 = await factory.create()
    user2 = await factory.create()

    assert user1.id != user2.id
    assert user1.email != user2.email


@pytest.mark.asyncio
async def test_user_factory_create_batch(db_session):
    """Test that UserFactory can create multiple users at once."""
    factory = await create_user_factory(db_session)
    users = await factory.create_batch(5)

    assert len(users) == 5
    # Check all IDs are unique
    ids = {user.id for user in users}
    assert len(ids) == 5
    # Check all emails are unique
    emails = {user.email for user in users}
    assert len(emails) == 5


# Note: BotFactory and FlowFactory tests will be added when models are implemented
