from dataclasses import dataclass, asdict, field, replace
from abc import ABC
from typing import Any, Iterable, Self

from pydantic import BaseModel


@dataclass
class BaseEntity(ABC):
    """
    Abstract base class for all domain entities.

    Provides:
        - id with immutability protection
        - pure update via replace()
        - to_dict helpers
        - apply_dto for application layer sync
        - equality & hash based on id
    """

    id: int | None = field(default=None)

    # -------------------------------
    # Serialization
    # -------------------------------

    def to_dict(
            self,
            exclude_id: bool = False,
            exclude: Iterable[str] | None = None,
            **kwargs: Any
    ) -> dict:
        """
        Convert entity to a dictionary representation.

        Args:
            exclude_id: Exclude the `id` field.
            exclude: Iterable of fields to exclude.
            kwargs: Additional key/value pairs to override.

        Returns:
            dict
        """
        d = asdict(self)

        if exclude_id:
            d.pop("id", None)

        if exclude is not None:
            for f in exclude:
                d.pop(f, None)

        if kwargs:
            d.update(kwargs)

        return d

    # -------------------------------
    # State helpers
    # -------------------------------

    def is_new(self) -> bool:
        """Return True if entity is not persisted."""
        return self.id is None

    def apply_dto(self, dto: BaseModel, ignore_none: bool = True) -> None:
        """
        Mutating update — only used in application layer.

        NOTE: This breaks immutability, but still allowed for convenience.
        Recommended only for CRUD-like domains.
        """
        for key, value in dto.model_dump().items():
            if hasattr(self, key) and (not ignore_none or value is not None):
                setattr(self, key, value)

    def get_new_updated(self, updates: dict[str, Any]) -> Self:
        """
        Pure (immutable) update: return a new entity.

        Example:
            updated = entity.get_new_updated({"name": "new"})
        """
        return replace(self, **updates)

    # -------------------------------
    # Identity immutability
    # -------------------------------

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Prevent reassignment of `id` once set.
        """
        if name == "id" and getattr(self, "id", None) is not None:
            return
        super().__setattr__(name, value)

    # -------------------------------
    # Equality & hashing
    # -------------------------------

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        # Entity identity based on (class, id)
        return hash((self.__class__.__name__, self.id))
