from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from application.account.dto.auth.password_email import (
    AuthChangePasswordRequestDTO,
    AuthRecoverPasswordRequestDTO,
    AuthRegisterByEmailRequestDTO,
    AuthResetPasswordByCodeRequestDTO,
    AuthSetPasswordRequestDTO,
)
from application.account.dto.auth.request.oauth import AuthRequestOAuthDTO, OAuthProviderDataDTO
from application.account.dto.auth.request.registration import AuthRequestLoginDTO, RegistrationLoginProviderDataDTO
from application.account.use_cases.auth.auth import AuthUseCase
from core.enums.app.account.auth_provider import AuthProviderType
from interfaces.fast_api.routers.auth import (
    change_password,
    login,
    recover_password,
    register_by_email,
    reset_password_by_code,
    set_password_if_missing,
)


@pytest.mark.asyncio
async def test_register_by_email_sends_password_and_allows_login() -> None:
    sender_mock = AsyncMock()
    with patch("application.account.use_cases.auth.password_email.get_email_sender") as sender_factory, patch(
        "application.account.use_cases.auth.password_email.PasswordEmailAuthUseCase._generate_password",
        return_value="TempPass123",
    ):
        sender_factory.return_value.send_email = sender_mock
        result = await register_by_email(AuthRegisterByEmailRequestDTO(email="mail.signup@example.com"))

    assert result.status == "sent"
    assert result.email == "mail.signup@example.com"
    sender_mock.assert_awaited()

    auth = await login(
        AuthRequestLoginDTO(
            provider_type=AuthProviderType.PASSWORD,
            provider_data=RegistrationLoginProviderDataDTO(
                email="mail.signup@example.com",
                password="TempPass123",
            ),
        )
    )
    assert auth.account.id is not None


@pytest.mark.asyncio
async def test_register_by_email_fails_for_existing_email() -> None:
    sender_mock = AsyncMock()
    with patch("application.account.use_cases.auth.password_email.get_email_sender") as sender_factory, patch(
        "application.account.use_cases.auth.password_email.PasswordEmailAuthUseCase._generate_password",
        return_value="TempPass123",
    ):
        sender_factory.return_value.send_email = sender_mock
        await register_by_email(AuthRegisterByEmailRequestDTO(email="mail.dup@example.com"))

    with pytest.raises(HTTPException) as exc:
        await register_by_email(AuthRegisterByEmailRequestDTO(email="mail.dup@example.com"))
    assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_recover_password_sends_link_and_reset_works() -> None:
    sender_mock = AsyncMock()
    with patch("application.account.use_cases.auth.password_email.get_email_sender") as sender_factory, patch(
        "application.account.use_cases.auth.password_email.PasswordEmailAuthUseCase._generate_password",
        return_value="Initial123",
    ):
        sender_factory.return_value.send_email = sender_mock
        await register_by_email(AuthRegisterByEmailRequestDTO(email="mail.recover@example.com"))

    with patch("application.account.use_cases.auth.password_email.get_email_sender") as sender_factory, patch(
        "application.account.use_cases.auth.password_email.PasswordEmailAuthUseCase._generate_recovery_code",
        return_value="recovery-code-123",
    ):
        sender_factory.return_value.send_email = sender_mock
        result = await recover_password(AuthRecoverPasswordRequestDTO(email="mail.recover@example.com"))

    assert result.status == "sent"
    assert result.email == "mail.recover@example.com"
    assert sender_mock.await_args is not None
    sent_text = sender_mock.await_args.kwargs["text_body"]
    assert "recovery-code-123" in sent_text

    reset = await reset_password_by_code(
        AuthResetPasswordByCodeRequestDTO(
            code="recovery-code-123",
            password="Recovered123",
            confirm_password="Recovered123",
        )
    )
    assert reset.status == "reset"
    assert reset.email == "mail.recover@example.com"

    with pytest.raises(HTTPException):
        await reset_password_by_code(
            AuthResetPasswordByCodeRequestDTO(
                code="recovery-code-123",
                password="RecoveredXXX",
                confirm_password="RecoveredXXX",
            )
        )

    auth = await login(
        AuthRequestLoginDTO(
            provider_type=AuthProviderType.PASSWORD,
            provider_data=RegistrationLoginProviderDataDTO(
                email="mail.recover@example.com",
                password="Recovered123",
            ),
        )
    )
    assert auth.account.id is not None


@pytest.mark.asyncio
async def test_set_password_if_missing_for_oauth_account() -> None:
    oauth = await AuthUseCase().oauth_auth(
        AuthRequestOAuthDTO(
            provider_type=AuthProviderType.GOOGLE,
            provider_data=OAuthProviderDataDTO(
                provider_user_id="google-mail-set-1",
                email="oauth.set@example.com",
                username="oauth.set@example.com",
            ),
        )
    )
    assert oauth.account.id is not None
    account = await AuthUseCase().get_account_by_token(oauth.token)

    result = await set_password_if_missing(
        AuthSetPasswordRequestDTO(
            password="NewPass123",
            confirm_password="NewPass123",
        ),
        account=account,
    )
    assert result.status == "set"
    assert result.profile.provider_type == AuthProviderType.PASSWORD

    auth = await login(
        AuthRequestLoginDTO(
            provider_type=AuthProviderType.PASSWORD,
            provider_data=RegistrationLoginProviderDataDTO(
                email="oauth.set@example.com",
                password="NewPass123",
            ),
        )
    )
    assert auth.account.id == oauth.account.id


@pytest.mark.asyncio
async def test_change_password_for_authorized_account() -> None:
    sender_mock = AsyncMock()
    with patch("application.account.use_cases.auth.password_email.get_email_sender") as sender_factory, patch(
        "application.account.use_cases.auth.password_email.PasswordEmailAuthUseCase._generate_password",
        return_value="Initial123",
    ):
        sender_factory.return_value.send_email = sender_mock
        signup = await register_by_email(AuthRegisterByEmailRequestDTO(email="mail.change@example.com"))
    assert signup.status == "sent"

    auth = await login(
        AuthRequestLoginDTO(
            provider_type=AuthProviderType.PASSWORD,
            provider_data=RegistrationLoginProviderDataDTO(
                email="mail.change@example.com",
                password="Initial123",
            ),
        )
    )
    account = await AuthUseCase().get_account_by_token(auth.token)

    changed = await change_password(
        AuthChangePasswordRequestDTO(
            current_password="Initial123",
            password="Changed123",
            confirm_password="Changed123",
        ),
        account=account,
    )
    assert changed.status == "changed"

    with pytest.raises(HTTPException):
        await change_password(
            AuthChangePasswordRequestDTO(
                current_password="Wrong123",
                password="ChangedXXX",
                confirm_password="ChangedXXX",
            ),
            account=account,
        )

    relogin = await login(
        AuthRequestLoginDTO(
            provider_type=AuthProviderType.PASSWORD,
            provider_data=RegistrationLoginProviderDataDTO(
                email="mail.change@example.com",
                password="Changed123",
            ),
        )
    )
    assert relogin.account.id == auth.account.id
