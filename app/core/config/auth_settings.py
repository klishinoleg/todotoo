from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.enums.di.access_control import AccessTokenType, PasswordHasherType


class AuthSettings(BaseSettings):
    default_access_token_type: AccessTokenType = AccessTokenType.JWT
    default_password_hasher_type: PasswordHasherType = PasswordHasherType.BCRYPT

    access_token_secret_key: str = Field(
        default="",
        validation_alias=AliasChoices("AUTH_ACCESS_TOKEN_SECRET_KEY", "SYSTEM_ACCESS_TOKEN_SECRET_KEY"),
    )
    access_token_expire_minutes: int = Field(
        default=60,
        validation_alias=AliasChoices("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", "SYSTEM_ACCESS_TOKEN_EXPIRE_MINUTES"),
    )
    tg_bot_token: str = Field(
        default="",
        validation_alias=AliasChoices("AUTH_TG_BOT_TOKEN", "SYSTEM_TG_BOT_TOKEN", "TELEGRAM_BOT_TOKEN"),
    )

    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = ""

    apple_client_id: str = ""
    apple_team_id: str = ""
    apple_key_id: str = ""
    apple_private_key: str = ""
    apple_redirect_uri: str = ""

    facebook_app_id: str = ""
    facebook_app_secret: str = ""
    facebook_redirect_uri: str = ""

    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        env_file=Path(__file__).parents[2] / ".env",
        extra="ignore",
    )

