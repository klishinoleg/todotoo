from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.event.entities.event_occurrence_message import EventOccurrenceMessageEntity
from domain.event.repositories.event_occurrence_message import EventOccurrenceMessageFilter, \
    EventOccurrenceMessageRepository


class EventOccurrenceMessageService(
    BaseService[EventOccurrenceMessageEntity, EventOccurrenceMessageFilter, EventOccurrenceMessageRepository]
):
    """
    Application-level service for working with EventOccurrenceMessageEntity.

    Responsibilities:
    - Resolve correct EventOccurrenceMessageRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for message logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(EventOccurrenceMessageEntity, repository_type)
