from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from core.enums.app.account.auth_provider import AuthActionType, AuthProviderType


class OAuthAuthorizeUrlDTO(BaseModel):
    provider_type: AuthProviderType
    action_type: AuthActionType
    auth_url: str
    state: str


class OAuthCallbackDTO(BaseModel):
    code: str = Field(min_length=1)
    state: str | None = None
    action_type: AuthActionType | None = None
    redirect_uri: str | None = None
    user: dict[str, Any] | None = None
