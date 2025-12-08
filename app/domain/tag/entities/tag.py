from dataclasses import dataclass

from domain.base.entity import BaseEntity


@dataclass(slots=True, kw_only=True)
class TagEntity(BaseEntity):
    """
    Domain entity representing a tag.
    """

    name: str
    slug: str
    parent_id: int | None
    ordering: int
    is_active: bool
    icon: str | None = None
    icon_small: str | None = None
    icon_middle: str | None = None
