from typing import Optional, Type

from tortoise.transactions import in_transaction

from core.db import MASTER_CONNECTION
from core.di.repository import DIRepositoryTransaction
from core.enums.di.repository import RepositoryType
from infrastructure.repository.transaction import RepositoryTransactionManager, RepositoryTransaction


class TortoiseTransaction(RepositoryTransaction):
    def __init__(self) -> None:
        self._ctx = in_transaction(MASTER_CONNECTION)

    async def __aenter__(self) -> "TortoiseTransaction":
        self._conn = await self._ctx.__aenter__()
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[object],
    ) -> None:
        await self._ctx.__aexit__(exc_type, exc_val, exc_tb)


class TortoiseTransactionManager(RepositoryTransactionManager):
    """Transaction manager for Tortoise ORM."""

    def start(self) -> RepositoryTransaction:
        return TortoiseTransaction()


DIRepositoryTransaction.register(RepositoryType.TORTOISE, TortoiseTransactionManager)
