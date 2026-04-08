from __future__ import annotations

import time
from typing import Any, ClassVar

from core.di.fast_storage import DIFastStorageProvider
from core.enums.di.fast_storage import FastStorageType
from interfaces.fast_storage.fast_storage import FastStorage


class MemoryFastStorage(FastStorage):
    _store: ClassVar[dict[str, tuple[float, dict[str, Any]]]] = {}

    async def set_json(self, key: str, value: dict[str, Any], ttl_seconds: int) -> None:
        expires_at = time.time() + max(ttl_seconds, 1)
        self._store[key] = (expires_at, dict(value))

    async def get_json(self, key: str) -> dict[str, Any] | None:
        payload = self._store.get(key)
        if payload is None:
            return None
        expires_at, value = payload
        if expires_at < time.time():
            self._store.pop(key, None)
            return None
        return dict(value)

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)


DIFastStorageProvider.register(FastStorageType.MEMORY, MemoryFastStorage)
