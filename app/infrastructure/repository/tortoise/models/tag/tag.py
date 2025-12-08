from typing import TYPE_CHECKING, Callable, Awaitable

from tortoise import fields
from tortoise_imagefield import ImageField

from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class TagModel(BaseTortoiseModel):
    """
    Tortoise ORM model for TagEntity.
    """

    # Core fields
    name = fields.CharField(
        max_length=255,
        description="Human-readable tag name.",
    )
    slug = fields.CharField(
        max_length=255,
        unique=True,
        index=True,
        description="URL-friendly unique identifier.",
    )

    # Hierarchy
    parent: fields.ForeignKeyNullableRelation["TagModel"] = fields.ForeignKeyField(
        "models.TagModel",
        related_name="children",
        null=True,
        on_delete=fields.SET_NULL,
        description="Optional parent tag ID.",
    )

    ordering = fields.IntField(
        default=0,
        description="Ordering index for tag lists.",
    )

    # State
    is_active = fields.BooleanField(
        default=True,
        description="Logical active flag.",
    )

    # Icons
    icon = ImageField(directory_name="tag_icons", field_for_name="slug", null=True)

    if TYPE_CHECKING:
        parent_id: int | None
        get_icon_url: Callable[[], str]
        get_icon_webp: Callable[[int, int, str, bool | None], Awaitable[str]]

    class Meta:
        table = "tags"
        description = "Tag dictionary"
