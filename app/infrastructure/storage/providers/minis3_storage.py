from datetime import timedelta
from typing import cast
from urllib.parse import quote, urlparse

from core.config.settings import settings
from core.di.storage import DIStorageProvider
from core.enums.di.storage import StorageType
from interfaces.storage.storage import Storage


class MiniS3Storage(Storage):
    def __init__(self) -> None:
        from minio import Minio

        self._client = Minio(
            settings.storage.minis3_endpoint.strip(),
            access_key=settings.storage.minis3_access_key,
            secret_key=settings.storage.minis3_secret_key,
            secure=settings.storage.minis3_secure,
        )

    def get_url(self, key: str | None) -> str | None:
        if not key:
            return None

        if key.startswith("http://") or key.startswith("https://"):
            return key

        endpoint = settings.storage.minis3_public_endpoint.strip()
        if endpoint:
            if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
                scheme = "https" if settings.storage.minis3_secure else "http"
                endpoint = f"{scheme}://{endpoint}"
            endpoint = endpoint.rstrip("/")
            bucket = settings.storage.minis3_bucket.strip()
            safe_key = quote(key.lstrip("/"), safe="/")
            return f"{endpoint}/{bucket}/{safe_key}"

        # Private bucket path: return signed URL.
        expires = timedelta(hours=6)
        object_name = key.lstrip("/")
        signed_url = self._client.presigned_get_object(
            settings.storage.minis3_bucket,
            object_name,
            expires=expires,
        )
        return cast(str, signed_url)

    def to_key(self, value: str | None) -> str | None:
        if not value:
            return None

        if value.startswith("http://") or value.startswith("https://"):
            path = urlparse(value).path.lstrip("/")
            bucket_prefix = f"{settings.storage.minis3_bucket.strip('/')}/"
            if path.startswith(bucket_prefix):
                return path.removeprefix(bucket_prefix)
            return path

        bucket_prefix = f"{settings.storage.minis3_bucket.strip('/')}/"
        if value.startswith(bucket_prefix):
            return value.removeprefix(bucket_prefix)

        return value.lstrip("/")

DIStorageProvider.register(StorageType.MINIS3, MiniS3Storage)
