from __future__ import annotations

import hashlib
import io
import mimetypes
import urllib.parse
import urllib.request
from pathlib import Path

from application.account.constants.avatar import OAUTH_AVATAR_KEY_PREFIX, USER_AVATAR_KEY_PREFIX
from core.config.settings import settings
from core.enums.di.storage import StorageType
from core.enums.system.logger.message_levels import LogMessageLevel
from core.logger.logger import Logger

_MAX_AVATAR_SIZE_BYTES = 5 * 1024 * 1024


class AvatarStorageService:
    @staticmethod
    def _guess_extension(source_url: str, content_type: str | None) -> str:
        if content_type:
            guessed = mimetypes.guess_extension(content_type.split(";", 1)[0].strip())
            if guessed:
                return guessed
        parsed = urllib.parse.urlparse(source_url)
        suffix = Path(parsed.path).suffix.strip()
        if suffix:
            return suffix if suffix.startswith(".") else f".{suffix}"
        return ".jpg"

    @staticmethod
    def _download_image(source_url: str) -> tuple[bytes, str]:
        req = urllib.request.Request(source_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            content_type = str(resp.headers.get("Content-Type", "")).strip()
            data = resp.read(_MAX_AVATAR_SIZE_BYTES + 1)

        if not data:
            raise ValueError("Avatar download returned empty body")
        if len(data) > _MAX_AVATAR_SIZE_BYTES:
            raise ValueError("Avatar image is too large")
        return data, content_type

    @staticmethod
    def _build_key(source_url: str, content: bytes, content_type: str) -> str:
        digest = hashlib.sha256(content).hexdigest()[:24]
        ext = AvatarStorageService._guess_extension(source_url, content_type)
        return f"{OAUTH_AVATAR_KEY_PREFIX}/{digest}{ext}"

    @staticmethod
    def _save_local(key: str, content: bytes) -> None:
        root = settings.storage.get_local_upload_dir()
        target = (root / key).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    @staticmethod
    def _save_minis3(key: str, content: bytes, content_type: str) -> None:
        from minio import Minio

        client = Minio(
            settings.storage.minis3_endpoint.strip(),
            access_key=settings.storage.minis3_access_key,
            secret_key=settings.storage.minis3_secret_key,
            secure=settings.storage.minis3_secure,
        )
        client.put_object(
            bucket_name=settings.storage.minis3_bucket.strip(),
            object_name=key,
            data=io.BytesIO(content),
            length=len(content),
            content_type=content_type or "image/jpeg",
        )

    @staticmethod
    def _build_uploaded_key(filename: str | None, content: bytes, content_type: str | None) -> str:
        suffix = ""
        if filename:
            suffix = Path(filename).suffix.strip()
        if not suffix:
            suffix = AvatarStorageService._guess_extension(filename or "avatar", content_type)
        if suffix and not suffix.startswith("."):
            suffix = f".{suffix}"
        digest = hashlib.sha256(content).hexdigest()[:24]
        return f"{USER_AVATAR_KEY_PREFIX}/{digest}{suffix or '.jpg'}"

    async def persist_external_avatar(self, avatar_url: str | None) -> str | None:
        if not avatar_url:
            return avatar_url
        if not (avatar_url.startswith("http://") or avatar_url.startswith("https://")):
            return avatar_url

        try:
            content, content_type = self._download_image(avatar_url)
            key = self._build_key(avatar_url, content, content_type)
            if settings.storage.type == StorageType.LOCAL:
                self._save_local(key, content)
            elif settings.storage.type == StorageType.MINIS3:
                self._save_minis3(key, content, content_type)
            else:
                return avatar_url

            Logger.auth(
                "auth.avatar.persisted",
                storage_type=str(settings.storage.type),
                key=key,
            )
            return key
        except Exception as exc:
            Logger.auth(
                "auth.avatar.persist.error",
                level=LogMessageLevel.WARN,
                source=avatar_url,
                detail=str(exc),
            )
            return avatar_url

    async def persist_uploaded_avatar(
            self,
            *,
            filename: str | None,
            content_type: str | None,
            content: bytes,
    ) -> str | None:
        if not content:
            return None
        if len(content) > _MAX_AVATAR_SIZE_BYTES:
            return None

        key = self._build_uploaded_key(filename, content, content_type)
        if settings.storage.type == StorageType.LOCAL:
            self._save_local(key, content)
        elif settings.storage.type == StorageType.MINIS3:
            self._save_minis3(key, content, content_type or "image/jpeg")
        else:
            return None

        Logger.auth(
            "auth.avatar.uploaded",
            storage_type=str(settings.storage.type),
            key=key,
            filename=filename or "",
        )
        return key
