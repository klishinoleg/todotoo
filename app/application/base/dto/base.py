from typing import Self

from pydantic import BaseModel
from domain.base.entity import BaseEntity


class BaseEntityDTO(BaseModel):
    """
    Base DTO with generic logic for converting domain entities
    into DTO structures. All DTOs must inherit from this class.
    """

    @classmethod
    def from_entity(cls, entity: BaseEntity) -> Self:
        """
        Create DTO from a domain entity using only the fields declared
        in the DTO model. This avoids expensive full validation and
        ensures clean separation between domain and application layers.
        """
        dto_fields = cls.model_fields.keys()
        data = {}

        for field in dto_fields:
            value = getattr(entity, field)

            # Automatic value object → dict conversion
            if hasattr(value, "to_dict"):
                value = value.to_dict()

            data[field] = value

        return cls.model_validate(data)


class ItemDTO(BaseEntityDTO):
    """Detailed DTO representing a single entity."""
    id: int


class ListDTO(BaseEntityDTO):
    """Lightweight DTO used in listing endpoints."""
    id: int


class PaginatedListDTO(BaseModel):
    """
    Standardized DTO for paginated responses.
    Ensures a consistent structure across all list endpoints.
    """
    items: list[ListDTO]
    total: int
    page: int
    per_page: int


class ResultDTO(BaseModel):
    """
    General-purpose result DTO for operations that do not return an entity.
    Commonly used for create/update/delete actions or confirmations.
    """
    success: bool
    message: str | None = None


class RequestDTO(BaseModel):
    """
    Base DTO for incoming data in application-level use cases.
    Defines the input contract for Coordinators (Use Cases).
    """
    pass


class ResponseDTO(BaseModel):
    """
    Base DTO for outgoing data from application-level use cases.
    Defines a predictable output structure for external interfaces.
    """
    pass
