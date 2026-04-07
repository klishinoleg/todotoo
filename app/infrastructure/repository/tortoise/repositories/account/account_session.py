from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.account.entities.account_session import AccountSessionEntity
from domain.account.repositories.account_session import (
    AccountSessionRepository,
    AccountSessionFilter,
)
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models import AccountSessionModel


class AccountSessionTortoiseRepository(
    AccountSessionRepository[QuerySet],
    BaseTortoiseRepository[
        AccountSessionEntity,
        AccountSessionFilter[QuerySet],
        AccountSessionModel
    ],
):
    """
    Tortoise ORM repository for AccountSessionEntity.
    Provides CRUD and filtered list functionality.
    """

    model: Type[AccountSessionModel] = AccountSessionModel
    entity_cls: Type[AccountSessionEntity] = AccountSessionEntity

    # ---------------------------------------
    # Mapping: Model → Entity
    # ---------------------------------------
    async def to_entity(self, model: AccountSessionModel) -> AccountSessionEntity:
        return AccountSessionEntity(
            id=model.id,
            account_id=model.account_id,
            requests=model.requests,
            started_at=model.started_at,
            closed_at=model.closed_at,
        )

    # ---------------------------------------
    # Mapping: Entity → Model for DB insert/update
    # ---------------------------------------
    def from_entity(self, entity: AccountSessionEntity) -> AccountSessionModel:
        payload: dict[str, object] = {
            "account_id": entity.account_id,
            "requests": entity.requests,
            "started_at": entity.started_at,
            "closed_at": entity.closed_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


# Register in DI
DIRepository.register(AccountSessionEntity, AccountSessionTortoiseRepository, RepositoryType.TORTOISE)
