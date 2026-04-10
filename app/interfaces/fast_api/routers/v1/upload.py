from __future__ import annotations

import hashlib
import io
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from core.config.settings import settings
from core.enums.di.storage import StorageType
from core.storage import get_storage
from domain.account.entities.account import AccountEntity
from interfaces.fast_api.deps.account import get_current_account

router = APIRouter(prefix="/uploads", tags=["v1/uploads"])

_MAX_IMAGE_BYTES = 10 * 1024 * 1024
_MAX_FILE_BYTES = 50 * 1024 * 1024
_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


class UploadResponseDTO(BaseModel):
    url: str
    preview_url: str | None = None
    content_type: str
    size: int


def _require_account(account: AccountEntity) -> None:
    if account.id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")


def _build_key(prefix: str, filename: str | None, content: bytes, content_type: str | None) -> str:
    digest = hashlib.sha256(content).hexdigest()[:24]
    suffix = ""
    if filename:
        suffix = Path(filename).suffix.strip()
    if not suffix and content_type:
        guessed = mimetypes.guess_extension(content_type.split(";", 1)[0].strip())
        suffix = guessed or ""
    if suffix and not suffix.startswith("."):
        suffix = f".{suffix}"
    if not suffix:
        suffix = ".bin"
    date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"{prefix}/{date_part}/{digest}{suffix}"


def _save_local(key: str, content: bytes) -> None:
    root = settings.storage.get_local_upload_dir()
    target = (root / key).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def _save_minis3(key: str, content: bytes, content_type: str | None) -> None:
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
        content_type=content_type or "application/octet-stream",
    )


def _store(key: str, content: bytes, content_type: str | None) -> None:
    if settings.storage.type == StorageType.LOCAL:
        _save_local(key, content)
        return
    if settings.storage.type == StorageType.MINIS3:
        _save_minis3(key, content, content_type)
        return
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unsupported storage type")


@router.post("/images/", response_model=UploadResponseDTO)
async def upload_image(
        file: UploadFile = File(...),
        account: AccountEntity = Depends(get_current_account),
) -> UploadResponseDTO:
    _require_account(account)
    content = await file.read()
    content_type = (file.content_type or "").strip().lower()
    if content_type not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unsupported image type")
    if len(content) == 0 or len(content) > _MAX_IMAGE_BYTES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid image size")

    key = _build_key("images", file.filename, content, content_type)
    _store(key, content, content_type)
    url = get_storage().get_url(key)
    if not url:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to build file URL")
    return UploadResponseDTO(url=url, preview_url=url, content_type=content_type, size=len(content))


@router.post("/files/", response_model=UploadResponseDTO)
async def upload_file(
        file: UploadFile = File(...),
        account: AccountEntity = Depends(get_current_account),
) -> UploadResponseDTO:
    _require_account(account)
    content = await file.read()
    content_type = (file.content_type or "application/octet-stream").strip().lower()
    if len(content) == 0 or len(content) > _MAX_FILE_BYTES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid file size")

    key = _build_key("files", file.filename, content, content_type)
    _store(key, content, content_type)
    url = get_storage().get_url(key)
    if not url:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Failed to build file URL")
    return UploadResponseDTO(url=url, preview_url=None, content_type=content_type, size=len(content))
