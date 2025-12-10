from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.event.entities.event import EventEntity
from domain.event.repositories.event import EventFilter, EventRepository


class EventService(BaseService[EventEntity, EventFilter, EventRepository]):
    """
    Application-level service for working with EventEntity.

    Responsibilities:
    - Resolve correct EventRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for event logic
    """

    def __init__(self, repository_type: RepositoryType | None = None) -> None:
        super().__init__(EventEntity, repository_type)
