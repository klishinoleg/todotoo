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
    sub: str | None = None

    email: str | None = None
    email_verified: bool = False

    username: str | None = None
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    picture: str | dict[str, Any] | None = None
    raw_data: dict[str, Any] | None = None

    # Telegram Web Login support
    id: int | None = None
    photo_url: str | None = None
    auth_date: int | str | None = None
    hash: str | None = None

    @model_validator(mode="after")
    def normalize_provider_fields(self) -> "OAuthProviderDataDTO":
        if not self.provider_user_id:
            if self.sub:
                self.provider_user_id = self.sub
            elif self.id is not None:
                self.provider_user_id = str(self.id)

        if not self.first_name and self.given_name:
            self.first_name = self.given_name
        if not self.last_name and self.family_name:
            self.last_name = self.family_name
        if self.name and (not self.first_name or not self.last_name) and " " in self.name:
            first, _, last = self.name.partition(" ")
            if not self.first_name:
                self.first_name = first
            if not self.last_name:
                self.last_name = last
        if not self.avatar_url:
            if isinstance(self.picture, str):
                self.avatar_url = self.picture
            elif isinstance(self.picture, dict):
                picture_data = self.picture.get("data")
                if isinstance(picture_data, dict):
                    url = picture_data.get("url")
                    if isinstance(url, str):
                        self.avatar_url = url
            if not self.avatar_url:
                self.avatar_url = self.photo_url

        return self


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


class AuthRequestOAuthDTO(AuthRequestDTO[OAuthProviderDataDTO]):
    action_type: AuthActionType | None = Field(default=None)
    provider_type: AuthProviderType

    @model_validator(mode="after")
    def validate_provider_type(self) -> "AuthRequestOAuthDTO":
        if self.provider_type not in OAUTH_PROVIDER_TYPES:
            raise ValueError("provider_type must be one of oauth providers")
        return self
