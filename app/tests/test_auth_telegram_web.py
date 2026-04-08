from __future__ import annotations

import hashlib
import hmac

import pytest

from application.account.dto.auth.request.oauth import AuthRequestOAuthDTO, OAuthProviderDataDTO
from core.config.settings import settings
from core.enums.app.account.auth_provider import AuthProviderType
from fastapi import HTTPException
from infrastructure.repository.tortoise.models.account.account import AccountModel
from infrastructure.repository.tortoise.models.account.account_auth_profile import AccountAuthProfileModel
from interfaces.fast_api.routers.auth import oauth


def _build_telegram_web_hash(payload: dict[str, object]) -> str:
    lines: list[str] = []
    for key in sorted(payload.keys()):
        value = payload[key]
        if value is None:
            continue
        lines.append(f"{key}={value}")
    data_check_string = "\n".join(lines)
    secret = hashlib.sha256(settings.auth.tg_bot_token.encode()).digest()
    return hmac.new(secret, data_check_string.encode(), hashlib.sha256).hexdigest()


@pytest.mark.asyncio
async def test_telegram_web_oauth_creates_account_and_reuses_existing() -> None:
    base_payload: dict[str, object] = {
        "id": 777000111,
        "first_name": "Oleg",
        "last_name": "Klishin",
        "username": "klishinoleg_web",
        "photo_url": "https://example.com/tg-avatar.jpg",
        "auth_date": 1775580000,
    }
    telegram_hash = _build_telegram_web_hash(base_payload)

    request = AuthRequestOAuthDTO(
        provider_type=AuthProviderType.TELEGRAM_WEB,
        provider_data=OAuthProviderDataDTO.model_validate(
            {
                **base_payload,
                "hash": telegram_hash,
            }
        ),
    )

    first = await oauth(request)
    second = await oauth(request)

    assert first.account.id is not None
    assert first.account.username == "klishinoleg_web"
    assert first.auth.provider_type == AuthProviderType.TELEGRAM_WEB
    assert first.auth.provider_id == str(base_payload["id"])
    assert second.account.id == first.account.id
    assert second.auth.id == first.auth.id

    assert await AccountModel.all().count() == 1
    assert await AccountAuthProfileModel.all().count() == 1


@pytest.mark.asyncio
async def test_telegram_web_oauth_rejects_invalid_hash() -> None:
    request = AuthRequestOAuthDTO(
        provider_type=AuthProviderType.TELEGRAM_WEB,
        provider_data=OAuthProviderDataDTO.model_validate(
            {
                "id": 777000222,
                "first_name": "Bad",
                "username": "bad_hash_user",
                "auth_date": 1775580000,
                "hash": "invalid_hash",
            }
        ),
    )

    with pytest.raises(HTTPException) as exc:
        await oauth(request)

    assert exc.value.status_code == 422
