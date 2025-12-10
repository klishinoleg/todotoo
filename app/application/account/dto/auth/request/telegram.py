# -----------------------------
# Telegram DTO structures
# -----------------------------
from pydantic import BaseModel, Field

from application.account.dto.auth.request.base import AuthRequestDTO
from core.enums.app.account.auth_provider import AuthProviderType


class TelegramUserDTO(BaseModel):
    """DTO describing a Telegram user."""
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None


class TelegramChatDTO(BaseModel):
    """DTO describing a Telegram chat."""
    id: int
    type: str
    title: str | None = None
    username: str | None = None
    photo_url: str | None = None


class TelegramAuthProviderDataDTO(BaseModel):
    """
    Application-level DTO for Telegram authentication.
    This mirrors TelegramInitData but is used only at the application boundary.
    """
    user: TelegramUserDTO
    query_id: str | None = None
    receiver: TelegramUserDTO | None = None
    chat: TelegramChatDTO | None = None
    chat_type: str | None = None
    chat_instance: str | None = None
    start_param: str | None = None
    can_send_after: int | None = None

    auth_date: str
    hash: str | None = None
    signature: str | None = None
    init_data: str


class AuthRequestTelegramDTO(AuthRequestDTO[TelegramAuthProviderDataDTO]):
    provider_type: AuthProviderType = Field(default=AuthProviderType.TELEGRAM)
