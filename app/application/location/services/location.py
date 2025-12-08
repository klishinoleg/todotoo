from core.enums.di.repository import RepositoryType
from application.base.service.base_service import BaseService

from domain.location.entities.location import LocationEntity
from domain.location.repositories.location import LocationRepository, LocationFilter


class LocationService(BaseService[LocationEntity, LocationFilter]):
    """
    Application-level service for working with LocationEntity.

    Responsibilities:
    - Resolve correct LocationRepository via DI
    - Provide CRUD and filtered_list operations (inherited from BaseService)
    - Add application-level validation and helper methods for location logic
    """

    def __init__(self, repository_type: RepositoryType | None = None):
        super().__init__(LocationEntity, repository_type)
