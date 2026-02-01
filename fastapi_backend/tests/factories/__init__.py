"""Test factories for creating test data.

This module provides async factory functions for generating test data
in a clean and maintainable way for async SQLAlchemy sessions.

Usage:
    from tests.factories import create_user_factory, AsyncUserFactory

    # Using convenience function
    factory = await create_user_factory(db_session)
    user = await factory.create(email="test@example.com")

    # Or using class directly
    factory = AsyncUserFactory(db_session)
    user = await factory.create()

    # Create multiple users
    users = await factory.create_batch(5, is_superuser=True)
"""

from tests.factories.user_factory import AsyncUserFactory, create_user_factory

__all__ = ["AsyncUserFactory", "create_user_factory"]

# Note: BotFactory and FlowFactory will be exported here when models are implemented
