# app/core/config/system_settings.py
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.enums.dev.enviroment_types import EnviromentTypes
from core.enums.di.access_control import AccessTokenType, PasswordHasherType
from core.enums.di.repository import RepositoryType


class SystemSettings(BaseSettings):
    """System-level configuration: domain, URLs, API tokens, environment, etc."""

    env_type: EnviromentTypes = EnviromentTypes.DEVELOPMENT
    default_language: str = "en"
    email_domain: str = ""
    web_app_url: str = ""
    allowed_origins: str = "*"
    secret_key: str = ""
    images_upload_dir: str = "uploads"
    images_upload_url: str = "uploads"
    locales_dir: str = "locales"
    api_v1: str = "/api/v1"
    ws_v1: str = "/ws/v1"
    server_url: str = ""
    tg_bot_token: str = ""
    languages: str = "en|ru"
    default_timezone: str = "Europe/Belgrade"
    default_repository_type: RepositoryType = RepositoryType.TORTOISE
    default_access_token_type: AccessTokenType = AccessTokenType.JWT
    default_password_hasher_type: PasswordHasherType = PasswordHasherType.BCRYPT
    access_token_secret_key: str = ""
    access_token_expire_minutes: int = 60
    geo_srid: int = 4326

    def get_languages(self) -> tuple[tuple[str, str], ...]:
        return tuple(lang for lang in (
            ("en", "English"),
            ("zh", "中文"),
            ("es", "Español"),
            ("ar", "العربية"),
            ("hi", "हिंदी"),
            ("fr", "Français"),
            ("ru", "Русский"),
            ("pt", "Português"),
            ("bn", "বাংলা"),
            ("de", "Deutsch"),
            ("ja", "日本語"),
            ("ko", "한국어"),
            ("it", "Italiano"),
            ("tr", "Türkçe"),
            ("nl", "Nederlands"),
        ) if lang[0] in self.languages.split("|"))

    def get_upload_dir(self) -> Path:
        path = Path(__file__).parent.parent / self.images_upload_dir
        path.mkdir(exist_ok=True)
        return path

    def get_locales_dir(self) -> Path:
        path = Path(__file__).parent.parent / self.locales_dir
        path.mkdir(exist_ok=True)
        return path

    model_config = SettingsConfigDict(
        env_prefix="SYSTEM_",
        extra="ignore"
    )
