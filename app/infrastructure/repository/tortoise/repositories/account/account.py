from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.storage import get_storage
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
        storage = get_storage()
        avatar = storage.get_url(model.avatar)
        return AccountEntity(
            id=model.id,
            username=model.username,
            public_name=model.public_name,
            email=model.email,
            language=model.language,
            is_online=model.is_online,
            avatar=avatar,
            avatar_small=avatar,
            avatar_medium=avatar,
            avatar_large=avatar,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # ---------------------------------------
    # Mapping: Entity → Model for DB insert/update
    # ---------------------------------------
    def from_entity(self, entity: AccountEntity) -> AccountModel:
        storage = get_storage()
        username = str(entity.username or "").strip()
        if not username:
            email = str(entity.email or "").strip()
            username = email or "oauth:user"
        payload: dict[str, object] = {
            "username": username,
            "public_name": entity.public_name,
            "email": entity.email,
            "language": entity.language,
            "is_online": entity.is_online,
            "avatar": storage.to_key(entity.avatar),
            "is_active": entity.is_active,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(AccountEntity, AccountTortoiseRepository, RepositoryType.TORTOISE)
