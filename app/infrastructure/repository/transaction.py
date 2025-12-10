from abc import ABC, abstractmethod
from typing import Protocol, Self, Type, Optional


class RepositoryTransaction(Protocol):
    async def __aenter__(self) -> Self:
        ...

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[object],
    ) -> None:
        ...


class RepositoryTransactionManager(ABC):
    """Abstract transaction manager."""

    @abstractmethod
    def start(self) -> RepositoryTransaction:
        """Start a new transaction."""
        ...
