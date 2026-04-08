from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from application.account.dto.account_auth_profile import AccountAuthProfileDTO
from core.enums.app.account.auth_provider import AuthActionType
from core.enums.app.account.auth_provider import AuthProviderType


class AuthProfileLinkRequestDTO(BaseModel):
    provider_type: AuthProviderType
    provider_data: dict[str, Any] = Field(default_factory=dict)
    confirm_merge: bool = False


class AuthPasswordProfileLinkRequestDTO(BaseModel):
    email: str
    password: str
    confirm_password: str | None = None
    public_name: str | None = None
    language_code: str | None = None
    confirm_merge: bool = False


class AuthProfileLinkResponseDTO(BaseModel):
    status: Literal["linked", "already_linked", "confirmation_required"]
    profile: AccountAuthProfileDTO | None = None
    merged_account_id: int | None = None
    merged_account_deleted: bool = False
    operation_code: str | None = None
    detail: str | None = None


class AuthProfileDeleteResponseDTO(BaseModel):
    status: Literal["deleted"]
    profile_id: int


class AuthProfileOAuthCallbackLinkRequestDTO(BaseModel):
    code: str = Field(min_length=1)
    state: str | None = None
    action_type: AuthActionType | None = None
    redirect_uri: str | None = None
    user: dict[str, Any] | None = None
    confirm_merge: bool = False


class AuthProfileLinkConfirmRequestDTO(BaseModel):
    operation_code: str = Field(min_length=8)
