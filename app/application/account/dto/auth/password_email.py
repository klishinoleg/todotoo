from pydantic import BaseModel, Field

from application.account.dto.account_auth_profile import AccountAuthProfileDTO


class AuthRegisterByEmailRequestDTO(BaseModel):
    email: str
    public_name: str | None = None
    language_code: str | None = None


class AuthRecoverPasswordRequestDTO(BaseModel):
    email: str


class AuthSetPasswordRequestDTO(BaseModel):
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)


class AuthChangePasswordRequestDTO(BaseModel):
    current_password: str = Field(min_length=6)
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)


class AuthResetPasswordByCodeRequestDTO(BaseModel):
    code: str = Field(min_length=8)
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)


class AuthMailPasswordResponseDTO(BaseModel):
    status: str
    email: str


class AuthSetPasswordResponseDTO(BaseModel):
    status: str
    profile: AccountAuthProfileDTO
