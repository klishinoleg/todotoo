from __future__ import annotations

from io import BytesIO
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers

from application.account.dto.profile import ProfileUpdateRequestDTO
from application.account.dto.auth.request.oauth import AuthRequestOAuthDTO, OAuthProviderDataDTO
from application.account.use_cases.auth.auth import AuthUseCase
from core.enums.app.account.auth_provider import AuthProviderType
from interfaces.fast_api.routers.auth import (
    delete_profile_avatar,
    get_profile,
    update_profile,
    upload_profile_avatar,
)


@pytest.mark.asyncio
async def test_profile_update_public_name_and_language() -> None:
    auth = await AuthUseCase().oauth_auth(
        AuthRequestOAuthDTO(
            provider_type=AuthProviderType.GOOGLE,
            provider_data=OAuthProviderDataDTO(
                provider_user_id="google-profile-1",
                email="profile1@example.com",
                username="profile1@example.com",
            ),
        )
    )
    account = await AuthUseCase().get_account_by_token(auth.token)

    updated = await update_profile(
        ProfileUpdateRequestDTO(public_name="New Name", language="ru"),
        account=account,
    )
    assert updated.public_name == "New Name"
    assert updated.language == "ru"

    current = await get_profile(account=account)
    assert current.id == updated.id


@pytest.mark.asyncio
async def test_profile_update_invalid_language_returns_422() -> None:
    auth = await AuthUseCase().oauth_auth(
        AuthRequestOAuthDTO(
            provider_type=AuthProviderType.GOOGLE,
            provider_data=OAuthProviderDataDTO(
                provider_user_id="google-profile-2",
                email="profile2@example.com",
                username="profile2@example.com",
            ),
        )
    )
    account = await AuthUseCase().get_account_by_token(auth.token)

    with pytest.raises(HTTPException) as exc:
        await update_profile(
            ProfileUpdateRequestDTO(language="xx"),
            account=account,
        )
    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_profile_avatar_upload_and_delete() -> None:
    auth = await AuthUseCase().oauth_auth(
        AuthRequestOAuthDTO(
            provider_type=AuthProviderType.GOOGLE,
            provider_data=OAuthProviderDataDTO(
                provider_user_id="google-profile-3",
                email="profile3@example.com",
                username="profile3@example.com",
            ),
        )
    )
    account = await AuthUseCase().get_account_by_token(auth.token)

    file = UploadFile(
        file=BytesIO(b"fake-image-bytes"),
        filename="avatar.jpg",
        headers=Headers({"content-type": "image/jpeg"}),
    )
    with patch(
            "application.account.services.avatar_storage.AvatarStorageService.persist_uploaded_avatar",
            new=AsyncMock(return_value="avatars/user/test-avatar.jpg"),
    ):
        uploaded = await upload_profile_avatar(file=file, account=account)
    assert uploaded.avatar is not None

    deleted = await delete_profile_avatar(account=account)
    assert deleted.avatar is None
