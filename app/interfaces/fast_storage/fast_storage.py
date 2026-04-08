from abc import ABC, abstractmethod
from typing import Any


class FastStorage(ABC):
    @abstractmethod
    async def set_json(self, key: str, value: dict[str, Any], ttl_seconds: int) -> None:
        ...

    @abstractmethod
    async def get_json(self, key: str) -> dict[str, Any] | None:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...
