from typing import Type

from tortoise.queryset import QuerySet

from core.di.auth import DIAuthProviderData
from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.account.entities.account_auth_profile import AccountAuthProfileEntity
from domain.account.repositories.account_auth_profile import (
    AccountAuthProfileFilter,
    AccountAuthProfileRepository,
)
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.account.account_auth_profile import (
    AccountAuthProfileModel,
)


class AccountAuthProfileTortoiseRepository(
    AccountAuthProfileRepository[QuerySet],
    BaseTortoiseRepository[
        AccountAuthProfileEntity,
        AccountAuthProfileFilter[QuerySet],
        AccountAuthProfileModel,
    ],
):
    """
    Tortoise ORM repository for AccountAuthProfileEntity.
    Uses BaseTortoiseRepository for CRUD, filtering, pagination, etc.
    """

    model: Type[AccountAuthProfileModel] = AccountAuthProfileModel
    entity_cls: Type[AccountAuthProfileEntity] = AccountAuthProfileEntity

    # ---------------------------------------
    # Mapping: Model → Entity
    # ---------------------------------------
    async def to_entity(
            self, model: AccountAuthProfileModel
    ) -> AccountAuthProfileEntity:
        provider_data = DIAuthProviderData.get(
            model.provider_type,
            model.provider_data,
        )
        return AccountAuthProfileEntity(
            id=model.id,
            account_id=model.account_id,
            provider_type=model.provider_type,
            provider_id=model.provider_id,
            provider_data=provider_data,
            language_code=model.language_code,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # ---------------------------------------
    # Mapping: Entity → Model data for DB
    # ---------------------------------------
    def from_entity(self, entity: AccountAuthProfileEntity) -> AccountAuthProfileModel:
        payload: dict[str, object] = {
            "account_id": entity.account_id,
            "provider_type": entity.provider_type,
            "provider_id": entity.provider_id,
            "provider_data": entity.provider_data.serialize(),
            "language_code": entity.language_code,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


# Register in DI
DIRepository.register(AccountAuthProfileEntity, AccountAuthProfileTortoiseRepository, RepositoryType.TORTOISE)
