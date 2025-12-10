from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.event.entities.event_occurrence import EventOccurrenceEntity
from domain.event.repositories.event_occurrence import EventOccurrenceFilter, EventOccurrenceRepository


class EventOccurrenceService(BaseService[EventOccurrenceEntity, EventOccurrenceFilter, EventOccurrenceRepository]):
    """
    Application-level service for working with EventOccurrenceEntity.

    Responsibilities:
    - Resolve correct EventOccurrenceRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for occurrence logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(EventOccurrenceEntity, repository_type)
