"""Async factories for creating test data.

This module provides async factory classes for generating test data
in a clean and maintainable way for async SQLAlchemy sessions.

Note: Due to SQLAlchemy AsyncSession requirements, we use a custom
async factory approach rather than factory-boy's SQLAlchemyModelFactory.
"""

import uuid
from faker import Faker
from app.models import User
from fastapi_users.password import PasswordHelper


class AsyncUserFactory:
    """Async factory for creating User instances."""

    def __init__(self, session):
        """Initialize factory with a database session.

        Args:
            session: Async SQLAlchemy session
        """
        self.session = session
        self.faker = Faker()
        self.password_helper = PasswordHelper()

    async def create(self, **kwargs):
        """Create and persist a User instance.

        Args:
            **kwargs: Optional attributes to override defaults

        Returns:
            User: Created user instance
        """
        user_data = {
            "id": uuid.uuid4(),
            "email": kwargs.get("email", self.faker.email()),
            "hashed_password": kwargs.get(
                "hashed_password", self.password_helper.hash("TestPassword123#")
            ),
            "is_active": kwargs.get("is_active", True),
            "is_superuser": kwargs.get("is_superuser", False),
            "is_verified": kwargs.get("is_verified", True),
        }

        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def create_batch(self, count, **kwargs):
        """Create multiple User instances.

        Args:
            count: Number of users to create
            **kwargs: Optional attributes to override defaults

        Returns:
            list[User]: List of created user instances
        """
        users = []
        for _ in range(count):
            user = await self.create(**kwargs)
            users.append(user)
        return users


# Convenience function for creating factory in tests
async def create_user_factory(session):
    """Create a UserFactory instance for the given session.

    Usage:
        factory = await create_user_factory(db_session)
        user = await factory.create(email="test@example.com")
    """
    return AsyncUserFactory(session)


# Note: BotFactory and FlowFactory will be added when Bot and Flow models are implemented
# in future stories. These factories will be structured similarly with proper relationships.
