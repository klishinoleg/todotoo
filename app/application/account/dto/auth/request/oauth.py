from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field
from pydantic import model_validator

from application.account.dto.auth.request.base import AuthRequestDTO
from core.enums.app.account.auth_provider import AuthActionType, AuthProviderType

OAUTH_PROVIDER_TYPES = {
    AuthProviderType.GOOGLE,
    AuthProviderType.APPLE,
    AuthProviderType.FACEBOOK,
    AuthProviderType.TELEGRAM_WEB,
}


class OAuthProviderDataDTO(BaseModel):
    provider_user_id: str | None = None

    email: str | None = None
    email_verified: bool = False

    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    raw_data: dict[str, Any] | None = None

    # Telegram Web Login support
    id: int | None = None
    photo_url: str | None = None
    auth_date: int | str | None = None
    hash: str | None = None


class AuthRequestOAuthSignUpDTO(AuthRequestDTO[OAuthProviderDataDTO]):
    action_type: AuthActionType = Field(default=AuthActionType.REGISTER)
    provider_type: AuthProviderType

    @model_validator(mode="after")
    def validate_provider_type(self) -> "AuthRequestOAuthSignUpDTO":
        if self.provider_type not in OAUTH_PROVIDER_TYPES:
            raise ValueError("provider_type must be one of oauth providers")
        return self


class AuthRequestOAuthLoginDTO(AuthRequestDTO[OAuthProviderDataDTO]):
    action_type: AuthActionType = Field(default=AuthActionType.LOGIN)
    provider_type: AuthProviderType

    @model_validator(mode="after")
    def validate_provider_type(self) -> "AuthRequestOAuthLoginDTO":
        if self.provider_type not in OAUTH_PROVIDER_TYPES:
            raise ValueError("provider_type must be one of oauth providers")
        return self
