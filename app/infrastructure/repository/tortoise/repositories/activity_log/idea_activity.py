from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.activity_log.idea_activity_type import IdeaActivityTypeEnum
from domain.activity_log.entities.idea_activity import IdeaActivityEntity
from domain.activity_log.repositories.idea_activity import IdeaActivityFilter, IdeaActivityRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.activity_log.idea_activity import IdeaActivityModel


class IdeaActivityTortoiseRepository(
    IdeaActivityRepository[QuerySet],
    BaseTortoiseRepository[IdeaActivityEntity, IdeaActivityFilter[QuerySet], IdeaActivityModel],
):
    model: Type[IdeaActivityModel] = IdeaActivityModel
    entity_cls: Type[IdeaActivityEntity] = IdeaActivityEntity

    async def to_entity(self, model: IdeaActivityModel) -> IdeaActivityEntity:
        return IdeaActivityEntity(
            id=model.id,
            idea_id=model.idea_id,
            account_id=model.account_id,
            type=IdeaActivityTypeEnum(model.type),
            payload=model.payload or {},
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: IdeaActivityEntity) -> IdeaActivityModel:
        payload: dict[str, object] = {
            "idea_id": entity.idea_id,
            "account_id": entity.account_id,
            "type": str(entity.type),
            "payload": entity.payload,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(IdeaActivityEntity, IdeaActivityTortoiseRepository, RepositoryType.TORTOISE)

