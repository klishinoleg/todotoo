from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
import sys

import pytest_asyncio
from tortoise import Tortoise

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from infrastructure.repository.tortoise.models.account.account import AccountModel
from infrastructure.repository.tortoise.models.account.account_auth_profile import AccountAuthProfileModel
from infrastructure.repository.tortoise.models.account.account_session import AccountSessionModel


TEST_TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://:memory:",
    },
    "apps": {
        "models": {
            "models": [
                "infrastructure.repository.tortoise.models.account.account",
                "infrastructure.repository.tortoise.models.account.account_auth_profile",
                "infrastructure.repository.tortoise.models.account.account_session",
            ],
            "default_connection": "default",
        }
    },
}


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_environment() -> AsyncGenerator[None, None]:
    # DI providers required by AuthUseCase flow.
    import infrastructure.access_control.password_hashers.bcrypt_password_hasher  # noqa: F401
    import infrastructure.access_control.token_providers.jwt_token_provider  # noqa: F401
    import infrastructure.auth.providers  # noqa: F401
    import infrastructure.repository.tortoise.transaction  # noqa: F401
    import infrastructure.repository.tortoise.base.filters.bool_filter  # noqa: F401
    import infrastructure.repository.tortoise.base.filters.equal_filter  # noqa: F401
    import infrastructure.repository.tortoise.base.filters.range_filter  # noqa: F401
    import infrastructure.repository.tortoise.base.filters.string_filters  # noqa: F401
    import infrastructure.repository.tortoise.repositories.account.account  # noqa: F401
    import infrastructure.repository.tortoise.repositories.account.account_auth_profile  # noqa: F401
    import infrastructure.repository.tortoise.repositories.account.account_session  # noqa: F401

    await Tortoise.init(config=TEST_TORTOISE_ORM)
    await Tortoise.generate_schemas()
    try:
        yield
    finally:
        await Tortoise.close_connections()


@pytest_asyncio.fixture(autouse=True)
async def clear_tables_between_tests() -> AsyncGenerator[None, None]:
    await AccountSessionModel.all().delete()
    await AccountAuthProfileModel.all().delete()
    await AccountModel.all().delete()
    yield
