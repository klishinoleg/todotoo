from __future__ import annotations

import hashlib
import hmac
import json
import urllib.parse

import pytest

from application.account.dto.auth.request.telegram import (
    AuthRequestTelegramDTO,
    TelegramAuthProviderDataDTO,
    TelegramUserDTO,
)
from core.config.settings import settings
from core.enums.app.account.auth_provider import AuthProviderType
from infrastructure.repository.tortoise.models.account.account import AccountModel
from infrastructure.repository.tortoise.models.account.account_auth_profile import AccountAuthProfileModel
from interfaces.fast_api.routers.auth import auth_via_telegram


def _build_init_data(user_payload: dict[str, object], auth_date: str, query_id: str) -> tuple[str, str]:
    data_without_hash = {
        "auth_date": auth_date,
        "query_id": query_id,
        "user": json.dumps(user_payload, separators=(",", ":"), ensure_ascii=False),
    }
    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(data_without_hash.items()))
    secret_key = hmac.new("WebAppData".encode(), settings.auth.tg_bot_token.encode(), hashlib.sha256).digest()
    digest = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    payload = dict(data_without_hash)
    payload["hash"] = digest
    return urllib.parse.urlencode(payload), digest


@pytest.mark.asyncio
async def test_telegram_auth_creates_account_and_reuses_existing() -> None:
    user_payload: dict[str, object] = {
        "id": 123456789,
        "is_bot": False,
        "first_name": "Oleg",
        "last_name": "Klishin",
        "username": "klishinoleg",
        "language_code": "ru",
        "is_premium": True,
        "allows_write_to_pm": True,
        "photo_url": None,
    }
    init_data, telegram_hash = _build_init_data(user_payload, auth_date="1775580000", query_id="AAE_TEST_QUERY")

    request = AuthRequestTelegramDTO(
        provider_type=AuthProviderType.TELEGRAM,
        provider_data=TelegramAuthProviderDataDTO(
            user=TelegramUserDTO.model_validate(user_payload),
            query_id="AAE_TEST_QUERY",
            auth_date="1775580000",
            hash=telegram_hash,
            signature=None,
            init_data=init_data,
        ),
    )

    first = await auth_via_telegram(request)
    second = await auth_via_telegram(request)

    assert first.account.id is not None
    assert first.account.username == "klishinoleg"
    assert first.auth.provider_type == AuthProviderType.TELEGRAM
    assert first.auth.provider_id == "123456789"
    assert second.account.id == first.account.id
    assert second.auth.id == first.auth.id

    assert await AccountModel.all().count() == 1
    assert await AccountAuthProfileModel.all().count() == 1
