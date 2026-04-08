from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.enums.di.fast_storage import FastStorageType


class FastStorageSettings(BaseSettings):
    type: FastStorageType = FastStorageType.MEMORY
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    operation_ttl_seconds: int = 900
    key_prefix: str = "todotoo:fast"

    model_config = SettingsConfigDict(
        env_prefix="FAST_STORAGE_",
        env_file=Path(__file__).parents[2] / ".env",
        extra="ignore",
    )
