from __future__ import annotations

import json
from typing import Any

from core.config.settings import settings
from core.di.fast_storage import DIFastStorageProvider
from core.enums.di.fast_storage import FastStorageType
from interfaces.fast_storage.fast_storage import FastStorage


class RedisFastStorage(FastStorage):
    def __init__(self) -> None:
        from redis.asyncio import Redis

        self._client = Redis(
            host=settings.fast_storage.redis_host,
            port=settings.fast_storage.redis_port,
            db=settings.fast_storage.redis_db,
            password=settings.fast_storage.redis_password or None,
            decode_responses=True,
        )
        self._prefix = settings.fast_storage.key_prefix.strip(":")

    def _key(self, key: str) -> str:
        return f"{self._prefix}:{key}"

    async def set_json(self, key: str, value: dict[str, Any], ttl_seconds: int) -> None:
        await self._client.set(self._key(key), json.dumps(value, ensure_ascii=False), ex=max(ttl_seconds, 1))

    async def get_json(self, key: str) -> dict[str, Any] | None:
        raw = await self._client.get(self._key(key))
        if not raw:
            return None
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
        return None

    async def delete(self, key: str) -> None:
        await self._client.delete(self._key(key))


DIFastStorageProvider.register(FastStorageType.REDIS, RedisFastStorage)
