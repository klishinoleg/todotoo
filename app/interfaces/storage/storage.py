from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def get_url(self, key: str | None) -> str | None:
        """Return public URL for stored object key."""
        ...

    @abstractmethod
    def to_key(self, value: str | None) -> str | None:
        """Normalize incoming value (key or URL) to storage object key."""
        ...
