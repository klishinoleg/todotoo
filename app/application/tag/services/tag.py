from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.tag.entities.tag import TagEntity
from domain.tag.repositories.tag import TagRepository, TagFilter


class TagService(BaseService[TagEntity, TagFilter]):
    """
    Application-level service for working with TagEntity.

    Responsibilities:
    - Resolve correct TagRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for tag logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(TagEntity, repository_type)
