from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.discussion.entities.discussion_attachment import DiscussionAttachmentEntity
from domain.discussion.repositories.discussion import DiscussionAttachmentFilter, DiscussionAttachmentRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.discussion.discussion_attachment import DiscussionAttachmentModel


class DiscussionAttachmentTortoiseRepository(
    DiscussionAttachmentRepository[QuerySet],
    BaseTortoiseRepository[
        DiscussionAttachmentEntity,
        DiscussionAttachmentFilter[QuerySet],
        DiscussionAttachmentModel,
    ],
):
    model: Type[DiscussionAttachmentModel] = DiscussionAttachmentModel
    entity_cls: Type[DiscussionAttachmentEntity] = DiscussionAttachmentEntity

    async def to_entity(self, model: DiscussionAttachmentModel) -> DiscussionAttachmentEntity:
        return DiscussionAttachmentEntity(
            id=model.id,
            message_id=model.message_id,
            file_url=model.file_url,
            file_type=model.file_type,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: DiscussionAttachmentEntity) -> DiscussionAttachmentModel:
        payload: dict[str, object] = {
            "message_id": entity.message_id,
            "file_url": entity.file_url,
            "file_type": entity.file_type,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(DiscussionAttachmentEntity, DiscussionAttachmentTortoiseRepository, RepositoryType.TORTOISE)

