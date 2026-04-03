from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.enums.di.storage import StorageType


class StorageSettings(BaseSettings):
    type: StorageType = StorageType.LOCAL

    local_upload_dir: str = "uploads"
    local_base_url: str = "/uploads"

    minis3_endpoint: str = "minis3:9000"
    minis3_public_endpoint: str = ""
    minis3_bucket: str = "todotoo"
    minis3_access_key: str = ""
    minis3_secret_key: str = ""
    minis3_secure: bool = False

    def get_local_upload_dir(self) -> Path:
        path = Path(__file__).parents[2] / self.local_upload_dir
        path.mkdir(parents=True, exist_ok=True)
        return path

    model_config = SettingsConfigDict(
        env_prefix="STORAGE_",
        extra="ignore",
    )

