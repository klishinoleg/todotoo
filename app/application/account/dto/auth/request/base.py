# application/account/dto/auth/request.py
from __future__ import annotations
from pydantic import BaseModel, Field
from core.enums.app.account.auth_provider import AuthProviderType, AuthActionType


# -----------------------------
# Main Auth Request DTO
# -----------------------------

class AuthRequestDTO[T: BaseModel](BaseModel):
    """
    Unified authentication request DTO.
    The provider_data field dynamically accepts different structures
    depending on provider_type.
    """
    provider_type: AuthProviderType
    action_type: AuthActionType | None = Field(default=None)
    provider_data: T
