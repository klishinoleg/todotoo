# app/core/config/system_settings.py
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.enums.dev.enviroment_types import EnviromentTypes
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
    languages: str = "en|ru"
    default_timezone: str = "Europe/Belgrade"
    default_repository_type: RepositoryType = RepositoryType.TORTOISE
    geo_srid: int = 4326

    def get_allowed_origins(self) -> list[str]:
        if self.allowed_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]

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
        configured_path = Path(self.locales_dir)
        if configured_path.is_absolute():
            path = configured_path
        else:
            path = Path(__file__).parents[2] / configured_path
        path.mkdir(parents=True, exist_ok=True)
        return path

    model_config = SettingsConfigDict(
        env_prefix="SYSTEM_",
        extra="ignore"
    )
