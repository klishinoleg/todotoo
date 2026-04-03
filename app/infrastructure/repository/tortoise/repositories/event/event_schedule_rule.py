from typing import Type

from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType
from domain.event.entities.event_schedule_rule import EventScheduleRuleEntity
from domain.event.repositories.event_schedule_rule import (
    EventScheduleRuleFilter,
    EventScheduleRuleRepository,
)
from infrastructure.repository.tortoise.base.repository import BaseTortoiseRepository
from infrastructure.repository.tortoise.models.event.event_schedule_rule import (
    EventScheduleRuleModel,
)


class EventScheduleRuleTortoiseRepository(
    EventScheduleRuleRepository[QuerySet],
    BaseTortoiseRepository[
        EventScheduleRuleEntity,
        EventScheduleRuleFilter[QuerySet],
        EventScheduleRuleModel,
    ],
):
    model: Type[EventScheduleRuleModel] = EventScheduleRuleModel
    entity_cls: Type[EventScheduleRuleEntity] = EventScheduleRuleEntity

    async def to_entity(self, model: EventScheduleRuleModel) -> EventScheduleRuleEntity:
        return EventScheduleRuleEntity(
            id=model.id,
            type=model.type,
            date=model.date,
            day_of_week=model.day_of_week,
            day_of_month=model.day_of_month,
            start_time=model.start_time,
            end_time=model.end_time,
        )

    def from_entity(self, entity: EventScheduleRuleEntity) -> EventScheduleRuleModel:
        return self.model(
            id=entity.id,
            type=entity.type,
            date=entity.date,
            day_of_week=entity.day_of_week,
            day_of_month=entity.day_of_month,
            start_time=entity.start_time,
            end_time=entity.end_time,
        )


DIRepository.register(EventScheduleRuleEntity, EventScheduleRuleTortoiseRepository, RepositoryType.TORTOISE)
