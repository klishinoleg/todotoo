from typing import Type

from tortoise.queryset import QuerySet

from core.config.settings import settings
from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.account.entities.account import AccountEntity
from domain.account.repositories.account import AccountRepository, AccountFilter
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models import AccountModel


class AccountTortoiseRepository(
    AccountRepository[QuerySet],
    BaseTortoiseRepository[AccountEntity, AccountFilter[QuerySet], AccountModel],
):
    """
    Tortoise ORM repository for AccountEntity.
    Uses BaseTortoiseRepository for filtering, CRUD, etc.
    """

    model: Type[AccountModel] = AccountModel
    entity_cls: Type[AccountEntity] = AccountEntity

    # ---------------------------------------
    # Mapping: Model → Entity
    # ---------------------------------------
    async def to_entity(self, model: AccountModel) -> AccountEntity:
        return AccountEntity(
            id=model.id,
            username=model.username,
            public_name=model.public_name,
            email=model.email,
            language=model.language,
            is_online=model.is_online,
            avatar=model.avatar,
            avatar_small=await model.get_avatar_webp(*settings.frontend.image_size_avatar_small),
            avatar_medium=await model.get_avatar_webp(*settings.frontend.image_size_avatar_medium),
            avatar_large=await model.get_avatar_webp(*settings.frontend.image_size_avatar_large),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # ---------------------------------------
    # Mapping: Entity → Model for DB insert/update
    # ---------------------------------------
    def from_entity(self, entity: AccountEntity) -> AccountModel:
        return self.model(
            id=entity.id,
            username=entity.username,
            public_name=entity.public_name,
            email=entity.email,
            language=entity.language,
            is_online=entity.is_online,
            avatar=entity.avatar,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


DIRepository.register(AccountEntity, AccountTortoiseRepository, RepositoryType.TORTOISE)
