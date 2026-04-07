from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from application.account.dto.auth.oauth_flow import OAuthCallbackDTO
from application.account.services.avatar_storage import AvatarStorageService
from core.config.settings import settings
from application.account.services.oauth_flow import OAuthFlowService
from core.enums.app.account.auth_provider import AuthProviderType
from core.enums.di.storage import StorageType
from infrastructure.repository.tortoise.models.account.account import AccountModel
from infrastructure.repository.tortoise.models.account.account_auth_profile import AccountAuthProfileModel
from interfaces.fast_api.routers.auth import oauth_callback


GOOGLE_PROVIDER_DATA = {
    "sub": "100967877670052977416",
    "email": "klishinoleg@gmail.com",
    "email_verified": True,
    "given_name": "Oleg",
    "family_name": "Klishin",
    "name": "Олег Клишин",
    "picture": "https://lh3.googleusercontent.com/a/mock",
    "raw_data": {
        "iss": "accounts.google.com",
        "aud": "mock-client-id.apps.googleusercontent.com",
    },
}


@pytest.mark.asyncio
async def test_google_callback_creates_account_and_then_reuses_existing() -> None:
    callback_dto = OAuthCallbackDTO(
        code="mock-google-code",
        state=None,
        redirect_uri="https://todotoo.ngrok.app/auth/google/callback",
        action_type=None,
        user=None,
    )

    with patch(
        "application.account.services.oauth_flow.OAuthFlowService.exchange_code_for_provider_data",
        new=AsyncMock(return_value=GOOGLE_PROVIDER_DATA),
    ), patch(
        "application.account.services.avatar_storage.AvatarStorageService.persist_external_avatar",
        new=AsyncMock(return_value="avatars/oauth/mock-avatar.jpg"),
    ):
        first = await oauth_callback(AuthProviderType.GOOGLE, callback_dto)
        second = await oauth_callback(AuthProviderType.GOOGLE, callback_dto)

    assert first.account.id is not None
    assert first.token
    assert first.account.username == "klishinoleg@gmail.com"
    assert first.account.avatar is not None
    assert first.auth.provider_type == AuthProviderType.GOOGLE
    assert first.auth.provider_id == GOOGLE_PROVIDER_DATA["sub"]

    # Second callback should log in to the same binding, not create duplicate rows.
    assert second.account.id == first.account.id
    assert second.auth.id == first.auth.id

    assert await AccountModel.all().count() == 1
    assert await AccountAuthProfileModel.all().count() == 1


def test_attach_raw_data_breaks_self_reference() -> None:
    payload: dict[str, object] = {"sub": "100967877670052977416", "email": "klishinoleg@gmail.com"}
    payload["raw_data"] = payload

    result = OAuthFlowService._attach_raw_data(payload)

    assert isinstance(result["raw_data"], dict)
    assert result["raw_data"] is not result
    assert result["raw_data"]["sub"] == "100967877670052977416"


@pytest.mark.asyncio
async def test_avatar_storage_persists_external_avatar_to_local(tmp_path: Path) -> None:
    service = AvatarStorageService()
    old_type = settings.storage.type
    old_upload_dir = settings.storage.local_upload_dir
    settings.storage.type = StorageType.LOCAL
    settings.storage.local_upload_dir = str(tmp_path)
    try:
        with patch.object(AvatarStorageService, "_download_image", return_value=(b"abc", "image/jpeg")):
            key = await service.persist_external_avatar("https://example.com/avatar.jpg")
        assert key is not None
        assert (tmp_path / key).is_file()
    finally:
        settings.storage.type = old_type
        settings.storage.local_upload_dir = old_upload_dir
