"""
Application service initialization and shutdown helpers.

This module is responsible for preparing all core services
required at application startup:

- Creating upload directories
- Initializing Tortoise ORM
- (Optionally) initializing Sentry, event publisher, etc.

It also provides a clean shutdown handler that closes
database connections and other async resources.
"""

import os

from core.db import init_tortoise, close_tortoise
from core.config.settings import settings
from core.enums.di.storage import StorageType


async def init_services(skip_publisher: bool = False) -> None:
    """
    Initialize all core application services.

    This function is executed during FastAPI startup and performs:
        - Ensuring filesystem paths exist
        - Initializing Tortoise ORM
        - (Optional) initializing publisher
        - (Optional) initializing Sentry

    Args:
        skip_publisher (bool):
            Skip initializing event publisher (useful for tests).
    """
    # Ensure storage providers are registered in DI.
    import infrastructure.storage  # noqa: F401

    if settings.storage.type == StorageType.LOCAL:
        upload_dir = settings.storage.get_local_upload_dir()
        os.makedirs(upload_dir, exist_ok=True)

    # Initialize database (Tortoise ORM)
    await init_tortoise()


async def shutdown_services(skip_publisher: bool = False) -> None:
    """
    Cleanly shut down all core services.

    This function is executed during FastAPI shutdown and performs:
        - Closing Tortoise ORM connections
        - Shutting down event publisher (optional)

    Args:
        skip_publisher (bool):
            Skip publisher shutdown (useful for tests).
    """

    # Close database connections
    await close_tortoise()
