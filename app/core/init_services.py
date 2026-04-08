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


def _bootstrap_di() -> None:
    # Storage providers
    import infrastructure.storage  # noqa: F401
    import infrastructure.fast_storage  # noqa: F401

    # Access control providers
    import infrastructure.access_control.password_hashers.bcrypt_password_hasher  # noqa: F401
    import infrastructure.access_control.token_providers.jwt_token_provider  # noqa: F401

    # Auth provider-data adapters
    import infrastructure.auth.providers  # noqa: F401

    # Transaction manager and query filters
    import infrastructure.repository.tortoise.transaction  # noqa: F401
    import infrastructure.repository.tortoise.base.filters.bool_filter  # noqa: F401
    import infrastructure.repository.tortoise.base.filters.equal_filter  # noqa: F401
    import infrastructure.repository.tortoise.base.filters.range_filter  # noqa: F401
    import infrastructure.repository.tortoise.base.filters.string_filters  # noqa: F401
    import infrastructure.repository.tortoise.base.filters.geometry_filter  # noqa: F401

    # Repositories used by current auth flow + legacy modules
    import infrastructure.repository.tortoise.repositories.account.account  # noqa: F401
    import infrastructure.repository.tortoise.repositories.account.account_auth_profile  # noqa: F401
    import infrastructure.repository.tortoise.repositories.account.account_session  # noqa: F401
    import infrastructure.repository.tortoise.repositories.location.location  # noqa: F401
    import infrastructure.repository.tortoise.repositories.tag.tag  # noqa: F401
    import infrastructure.repository.tortoise.repositories.event.event  # noqa: F401
    import infrastructure.repository.tortoise.repositories.event.event_member  # noqa: F401
    import infrastructure.repository.tortoise.repositories.event.event_occurrence  # noqa: F401
    import infrastructure.repository.tortoise.repositories.event.event_occurrence_message  # noqa: F401
    import infrastructure.repository.tortoise.repositories.event.event_schedule_rule  # noqa: F401


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
    _bootstrap_di()

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
