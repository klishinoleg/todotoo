from abc import ABC, abstractmethod
from typing import Protocol


class TokenProvider(Protocol):
    """Abstract interface for generating and verifying access tokens."""

    @abstractmethod
    def create_token(self, user_id: int, expire_minutes: int | None = None) -> str:
        """Create an access token."""
        ...

    @abstractmethod
    def decode_token(self, token: str) -> int:
        """Decode the token and return user_id or AccessControlException."""
        ...
