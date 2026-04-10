from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.idea_event.entities.event_reaction import IdeaEventReactionEntity
from domain.idea_event.repositories.event import IdeaEventReactionFilter, IdeaEventReactionRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.idea_event.event_reaction import IdeaEventReactionModel


class IdeaEventReactionTortoiseRepository(
    IdeaEventReactionRepository[QuerySet],
    BaseTortoiseRepository[
        IdeaEventReactionEntity,
        IdeaEventReactionFilter[QuerySet],
        IdeaEventReactionModel,
    ],
):
    model: Type[IdeaEventReactionModel] = IdeaEventReactionModel
    entity_cls: Type[IdeaEventReactionEntity] = IdeaEventReactionEntity

    async def to_entity(self, model: IdeaEventReactionModel) -> IdeaEventReactionEntity:
        return IdeaEventReactionEntity(
            id=model.id,
            event_id=model.event_id,
            account_id=model.account_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: IdeaEventReactionEntity) -> IdeaEventReactionModel:
        payload: dict[str, object] = {
            "event_id": entity.event_id,
            "account_id": entity.account_id,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(IdeaEventReactionEntity, IdeaEventReactionTortoiseRepository, RepositoryType.TORTOISE)

