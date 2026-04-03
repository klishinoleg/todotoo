from urllib.parse import quote, urlparse

from core.config.settings import settings
from core.di.storage import DIStorageProvider
from core.enums.di.storage import StorageType
from interfaces.storage.storage import Storage


class LocalStorage(Storage):
    def get_url(self, key: str | None) -> str | None:
        if not key:
            return None

        if key.startswith("http://") or key.startswith("https://") or key.startswith("/"):
            return key

        base_url = settings.storage.local_base_url.strip("/")
        return f"/{base_url}/{quote(key)}"

    def to_key(self, value: str | None) -> str | None:
        if not value:
            return None

        base_url = settings.storage.local_base_url.strip("/")
        prefix = f"/{base_url}/"

        if value.startswith("http://") or value.startswith("https://"):
            path = urlparse(value).path
            if path.startswith(prefix):
                return path.removeprefix(prefix).lstrip("/")
            return path.lstrip("/")

        if value.startswith(prefix):
            return value.removeprefix(prefix).lstrip("/")

        return value.lstrip("/")


DIStorageProvider.register(StorageType.LOCAL, LocalStorage)
