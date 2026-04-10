from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.idea_event.entities.event_comment import IdeaEventCommentEntity
from domain.idea_event.repositories.event import IdeaEventCommentFilter, IdeaEventCommentRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.idea_event.event_comment import IdeaEventCommentModel


class IdeaEventCommentTortoiseRepository(
    IdeaEventCommentRepository[QuerySet],
    BaseTortoiseRepository[
        IdeaEventCommentEntity,
        IdeaEventCommentFilter[QuerySet],
        IdeaEventCommentModel,
    ],
):
    model: Type[IdeaEventCommentModel] = IdeaEventCommentModel
    entity_cls: Type[IdeaEventCommentEntity] = IdeaEventCommentEntity

    async def to_entity(self, model: IdeaEventCommentModel) -> IdeaEventCommentEntity:
        return IdeaEventCommentEntity(
            id=model.id,
            event_id=model.event_id,
            account_id=model.account_id,
            text=model.text,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: IdeaEventCommentEntity) -> IdeaEventCommentModel:
        payload: dict[str, object] = {
            "event_id": entity.event_id,
            "account_id": entity.account_id,
            "text": entity.text,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(IdeaEventCommentEntity, IdeaEventCommentTortoiseRepository, RepositoryType.TORTOISE)

