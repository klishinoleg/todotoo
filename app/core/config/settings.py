# app/core/config/settings.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from .db_settings import DBSettings
from .frontend_settings import FrontendSettings
from .storage_settings import StorageSettings
from .system_settings import SystemSettings

class Settings(BaseSettings):
    """Main application settings combining domain-specific configs."""

    system: SystemSettings = SystemSettings()
    db: DBSettings = DBSettings()
    frontend: FrontendSettings = FrontendSettings()
    storage: StorageSettings = StorageSettings()
    admin_user_model: str = "AccountModel"
    admin_user_model_username_field: str = "username"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[2] / ".env",
        extra="ignore"
    )


settings = Settings()
