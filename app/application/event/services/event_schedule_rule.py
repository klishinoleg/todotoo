from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.event.entities.event_schedule_rule import EventScheduleRuleEntity
from domain.event.repositories.event_schedule_rule import EventScheduleRuleFilter, EventScheduleRuleRepository


class EventScheduleRuleService(
    BaseService[EventScheduleRuleEntity, EventScheduleRuleFilter, EventScheduleRuleRepository]):
    """
    Application-level service for working with EventScheduleRuleEntity.

    Responsibilities:
    - Resolve correct EventScheduleRuleRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for schedule rule logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(EventScheduleRuleEntity, repository_type)
