from __future__ import annotations
from typing import get_args, get_origin, Self
from pydantic import BaseModel, model_validator
from abc import ABC, abstractmethod


# ============================================================
# Base Filter Field
# ============================================================

class BaseFilterField[Q](BaseModel, ABC):
    """Field-level filter. Must implement filtering logic."""

    @abstractmethod
    def extend_query(self, name: str, query: Q) -> Q:
        """Apply filtering condition to query."""
        ...


# ============================================================
# Base Filter
# ============================================================

class BaseFilter[Q](BaseModel, ABC):
    """
    Base class for all domain filters.
    Ensures only BaseFilterField subclasses are used as fields.

    order_data:
        Optional list of ordering fields.
        Example:
            ["-created_at", "name"]
        Negative prefix = DESC.

    page:
        Page number for pagination (1-based).
        If None → no pagination applied.

    per_page:
        Items per page.
        If None → ignore pagination.
        Must be used only if 'page' is also provided.
    """
    order_data: list[str] | None = None
    page: int | None = None
    per_page: int | None = None

    # Validate that all model fields are BaseFilterField subclasses
    @model_validator(mode="after")
    def validate_filter_fields(self) -> Self:
        for name, value in self.__dict__.items():
            if value is None:
                # None fields are allowed (disabled filter)
                continue

            # Extract type from annotation
            ann = self.model_fields[name].annotation

            # Resolve Annotated, Optional, etc.
            origin = get_origin(ann)
            args = get_args(ann)
            field_type = None

            if origin is None:
                field_type = ann
            elif origin is list or origin is tuple:
                # probably [X] or (X)
                field_type = args[0]
            elif origin is type(None):
                continue
            else:
                # Optional[X], Union[X, None]
                for a in args:
                    if a is not type(None):
                        field_type = a

            if field_type is None:
                raise TypeError(f"Cannot resolve field type for filter field '{name}'")

            # Check inheritance
            if not issubclass(field_type, BaseFilterField):
                raise TypeError(
                    f"Filter field '{name}' must inherit from BaseFilterField, "
                    f"but received: {field_type}"
                )

        return self

    # --------------------------------------------------------

    def extend_query(self, query: Q) -> Q:
        """Apply all non-empty filter fields to query."""
        for name, value in self.__dict__.items():
            if value is None:
                continue

            # Each field applies its own filtering logic
            query = value.extend_query(name, query)

        return query
