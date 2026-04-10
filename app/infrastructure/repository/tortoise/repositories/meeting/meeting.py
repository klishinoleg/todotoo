from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.meeting.meeting_type import MeetingTypeEnum
from domain.meeting.entities.meeting import MeetingEntity
from domain.meeting.repositories.meeting import MeetingFilter, MeetingRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.meeting.meeting import MeetingModel


class MeetingTortoiseRepository(
    MeetingRepository[QuerySet],
    BaseTortoiseRepository[MeetingEntity, MeetingFilter[QuerySet], MeetingModel],
):
    model: Type[MeetingModel] = MeetingModel
    entity_cls: Type[MeetingEntity] = MeetingEntity

    async def to_entity(self, model: MeetingModel) -> MeetingEntity:
        return MeetingEntity(
            id=model.id,
            idea_id=model.idea_id,
            title=model.title,
            description=model.description,
            start_datetime=model.start_datetime,
            end_datetime=model.end_datetime,
            type=MeetingTypeEnum(model.type),
            location_name=model.location_name,
            latitude=model.latitude,
            longitude=model.longitude,
            meeting_url=model.meeting_url,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: MeetingEntity) -> MeetingModel:
        payload: dict[str, object] = {
            "idea_id": entity.idea_id,
            "title": entity.title,
            "description": entity.description,
            "start_datetime": entity.start_datetime,
            "end_datetime": entity.end_datetime,
            "type": str(entity.type),
            "location_name": entity.location_name,
            "latitude": entity.latitude,
            "longitude": entity.longitude,
            "meeting_url": entity.meeting_url,
            "created_by": entity.created_by,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(MeetingEntity, MeetingTortoiseRepository, RepositoryType.TORTOISE)

