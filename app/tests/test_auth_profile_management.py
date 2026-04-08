from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from application.account.dto.auth.profile_management import (
    AuthProfileLinkConfirmRequestDTO,
    AuthPasswordProfileLinkRequestDTO,
    AuthProfileOAuthCallbackLinkRequestDTO,
)
from application.account.dto.auth.request.oauth import AuthRequestOAuthDTO, OAuthProviderDataDTO
from application.account.dto.auth.request.registration import (
    AuthRequestSignUpDTO,
    RegistrationSignupProviderDataDTO,
)
from application.account.services.account import AccountService
from application.account.use_cases.auth.auth import AuthUseCase
from core.enums.app.account.auth_provider import AuthProviderType
from domain.account.entities.account import AccountEntity
from infrastructure.repository.tortoise.models.account.account import AccountModel
from interfaces.fast_api.routers.auth import (
    confirm_link_auth_profile,
    delete_profile,
    get_profiles,
    link_oauth_profile_callback,
    link_password_profile,
    signup,
)


async def _oauth_auth(provider_user_id: str, email: str, username: str) -> int:
    response = await AuthUseCase().oauth_auth(
        AuthRequestOAuthDTO(
            provider_type=AuthProviderType.GOOGLE,
            provider_data=OAuthProviderDataDTO(
                provider_user_id=provider_user_id,
                email=email,
                username=username,
            ),
        )
    )
    assert response.account.id is not None
    return response.account.id


async def _get_account(account_id: int) -> AccountEntity:
    account = await AccountService().get(account_id)
    assert account is not None
    return account


@pytest.mark.asyncio
async def test_link_password_profile_to_existing_account() -> None:
    account_id = await _oauth_auth("google-user-1", "user1@example.com", "user1@example.com")
    account = await _get_account(account_id)

    result = await link_password_profile(
        AuthPasswordProfileLinkRequestDTO(
            email="pass.user1@example.com",
            password="StrongPass123",
            confirm_password="StrongPass123",
        ),
        account=account,
    )

    assert result.status == "linked"
    assert result.profile is not None
    assert result.profile.provider_type == AuthProviderType.PASSWORD
    assert result.profile.account_id == account_id


@pytest.mark.asyncio
async def test_link_google_profile_via_callback_for_current_account() -> None:
    signup_result = await signup(
        AuthRequestSignUpDTO(
            provider_type=AuthProviderType.PASSWORD,
            provider_data=RegistrationSignupProviderDataDTO(
                email="owner.callback@example.com",
                password="StrongPass123",
                confirm_password="StrongPass123",
            ),
        )
    )
    assert signup_result.account.id is not None
    account = await _get_account(signup_result.account.id)

    callback_request = AuthProfileOAuthCallbackLinkRequestDTO(
        code="mock-google-code",
        redirect_uri="https://todotoo.ngrok.app/auth/google/callback",
    )
    with patch(
        "application.account.services.oauth_flow.OAuthFlowService.exchange_code_for_provider_data",
        new=AsyncMock(
            return_value={
                "sub": "google-link-user-1",
                "email": "owner.callback@gmail.com",
                "given_name": "Owner",
                "family_name": "Callback",
            }
        ),
    ):
        result = await link_oauth_profile_callback(AuthProviderType.GOOGLE, callback_request, account=account)

    assert result.status == "linked"
    assert result.profile is not None
    assert result.profile.provider_type == AuthProviderType.GOOGLE
    assert result.profile.account_id == account.id


@pytest.mark.asyncio
async def test_delete_profile_forbidden_for_last_profile() -> None:
    account_id = await _oauth_auth("google-user-2", "user2@example.com", "user2@example.com")
    account = await _get_account(account_id)

    linked = await link_password_profile(
        AuthPasswordProfileLinkRequestDTO(
            email="pass.user2@example.com",
            password="StrongPass123",
            confirm_password="StrongPass123",
        ),
        account=account,
    )
    assert linked.profile is not None

    deleted = await delete_profile(linked.profile.id, account=account)
    assert deleted.status == "deleted"
    assert deleted.profile_id == linked.profile.id

    profiles = await get_profiles(account=account)
    assert len(profiles) == 1

    with pytest.raises(HTTPException) as exc:
        await delete_profile(profiles[0].id, account=account)
    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_link_password_requires_merge_confirmation_then_merges() -> None:
    account_a_id = await _oauth_auth("google-user-3", "owner3@example.com", "owner3@example.com")
    account_a = await _get_account(account_a_id)

    await signup(
        AuthRequestSignUpDTO(
            provider_type=AuthProviderType.PASSWORD,
            provider_data=RegistrationSignupProviderDataDTO(
                email="conflict.user@example.com",
                password="StrongPass123",
                confirm_password="StrongPass123",
            ),
        )
    )
    assert await AccountModel.all().count() == 2

    pending = await link_password_profile(
        AuthPasswordProfileLinkRequestDTO(
            email="conflict.user@example.com",
            password="StrongPass123",
            confirm_password="StrongPass123",
            confirm_merge=False,
        ),
        account=account_a,
    )
    assert pending.status == "confirmation_required"
    assert pending.operation_code is not None
    assert pending.profile is None

    merged = await confirm_link_auth_profile(
        AuthProfileLinkConfirmRequestDTO(operation_code=pending.operation_code),
        account=account_a,
    )
    assert merged.status == "linked"
    assert merged.profile is not None
    assert merged.merged_account_deleted is True
    assert merged.merged_account_id is not None
    assert await AccountModel.all().count() == 1
