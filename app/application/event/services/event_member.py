from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.event.entities.event_member import EventMemberEntity
from domain.event.repositories.event_member import EventMemberRepository, EventMemberFilter


class EventMemberService(BaseService[EventMemberEntity, EventMemberFilter, EventMemberRepository]):
    """
    Application-level service for working with EventMemberEntity.

    Responsibilities:
    - Resolve correct EventMemberRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for event member logic
    """

    repository: EventMemberRepository

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(EventMemberEntity, repository_type)
