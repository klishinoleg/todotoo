from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from core.enums.app.calendar.calendar_item_type import CalendarItemTypeEnum
from domain.calendar.entities.calendar_item import CalendarItemEntity
from domain.calendar.repositories.calendar_item import CalendarItemFilter, CalendarItemRepository
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.calendar.calendar_item import CalendarItemModel


class CalendarItemTortoiseRepository(
    CalendarItemRepository[QuerySet],
    BaseTortoiseRepository[CalendarItemEntity, CalendarItemFilter[QuerySet], CalendarItemModel],
):
    model: Type[CalendarItemModel] = CalendarItemModel
    entity_cls: Type[CalendarItemEntity] = CalendarItemEntity

    async def to_entity(self, model: CalendarItemModel) -> CalendarItemEntity:
        return CalendarItemEntity(
            id=model.id,
            idea_id=model.idea_id,
            type=CalendarItemTypeEnum(model.type),
            ref_id=model.ref_id,
            start_datetime=model.start_datetime,
            end_datetime=model.end_datetime,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def from_entity(self, entity: CalendarItemEntity) -> CalendarItemModel:
        payload: dict[str, object] = {
            "idea_id": entity.idea_id,
            "type": str(entity.type),
            "ref_id": entity.ref_id,
            "start_datetime": entity.start_datetime,
            "end_datetime": entity.end_datetime,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }
        if entity.id is not None:
            payload["id"] = entity.id
        return self.model(**payload)


DIRepository.register(CalendarItemEntity, CalendarItemTortoiseRepository, RepositoryType.TORTOISE)

