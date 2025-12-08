# app/core/config/db_settings.py
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    """Database connection settings."""

    url: str = ""
    host: str = "localhost"
    pgb_host: str = "localhost"
    pgb_port: int = 6432
    port: int = 5432
    user: str = ""
    password: str = ""
    name: str = ""

    # Optional: direct URL or replica URL
    slave_url: str | None = None

    def get_db_url(self) -> str:
        return f"postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}?schema=public"

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=Path(__file__).parents[2] / ".env",
        extra="ignore"
    )
