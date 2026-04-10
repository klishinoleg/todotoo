from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.discussion.entities.discussion_message import DiscussionMessageEntity
from domain.discussion.repositories.discussion import DiscussionMessageFilter, DiscussionMessageRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.discussion.discussion_message import DiscussionMessageModel


class DiscussionMessageTortoiseRepository(
    DiscussionMessageRepository[QuerySet],
    BaseTortoiseRepository[
        DiscussionMessageEntity,
        DiscussionMessageFilter[QuerySet],
        DiscussionMessageModel,
    ],
):
    model: Type[DiscussionMessageModel] = DiscussionMessageModel
    entity_cls: Type[DiscussionMessageEntity] = DiscussionMessageEntity

    async def to_entity(self, model: DiscussionMessageModel) -> DiscussionMessageEntity:
        return DiscussionMessageEntity(
            id=model.id,
            discussion_id=model.discussion_id,
            account_id=model.account_id,
            text=model.text,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: DiscussionMessageEntity) -> DiscussionMessageModel:
        payload: dict[str, object] = {
            "discussion_id": entity.discussion_id,
            "account_id": entity.account_id,
            "text": entity.text,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(DiscussionMessageEntity, DiscussionMessageTortoiseRepository, RepositoryType.TORTOISE)

