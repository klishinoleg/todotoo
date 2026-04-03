# -----------------------------
# Registration DTO structures
# -----------------------------
from pydantic import BaseModel, Field

from application.account.dto.auth.request.base import AuthRequestDTO
from core.enums.app.account.auth_provider import AuthProviderType, AuthActionType


class RegistrationSignupProviderDataDTO(BaseModel):
    """DTO for registration (sign up)."""
    email: str
    password: str
    confirm_password: str
    public_name: str | None = None
    language_code: str | None = None
    ip: str | None = None
    user_agent: str | None = None
    start_param: str | None = None


class RegistrationLoginProviderDataDTO(BaseModel):
    """DTO for login via email-password."""
    email: str
    password: str
    ip: str | None = None
    user_agent: str | None = None


class AuthRequestSignUpDTO(AuthRequestDTO[RegistrationSignupProviderDataDTO]):
    provider_type: AuthProviderType = Field(default=AuthProviderType.PASSWORD)
    action_type: AuthActionType = Field(default=AuthActionType.REGISTER)


class AuthRequestLoginDTO(AuthRequestDTO[RegistrationLoginProviderDataDTO]):
    provider_type: AuthProviderType = Field(default=AuthProviderType.PASSWORD)
    action_type: AuthActionType = Field(default=AuthActionType.LOGIN)
