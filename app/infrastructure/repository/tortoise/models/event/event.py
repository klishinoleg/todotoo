from __future__ import annotations

from typing import TYPE_CHECKING, Awaitable, Callable

from postgis import Point, Polygon
from tortoise import fields
from tortoise_imagefield import ImageField

from core.config.settings import settings
from infrastructure.repository.tortoise.base.fields.point import PostGISPointField
from infrastructure.repository.tortoise.base.fields.polygon import PostGISPolygonField
from infrastructure.repository.tortoise.base.model import BaseTortoiseModel

if TYPE_CHECKING:
    from infrastructure.repository.tortoise.models.event.event_schedule_rule import EventScheduleRuleModel
    from infrastructure.repository.tortoise.models import AccountModel
    from infrastructure.repository.tortoise.models import LocationModel


class EventModel(BaseTortoiseModel):
    """
    Tortoise ORM model for EventEntity.

    Includes:
        - PostGIS point & polygon for spatial queries
        - Image field with derived webp helpers
    """

    # ---------------------------
    # Relations
    # ---------------------------
    account: fields.ForeignKeyRelation["AccountModel"] = fields.ForeignKeyField(
        "models.AccountModel",
        related_name="events",
        on_delete=fields.CASCADE,
        description="Owner account.",
    )

    location: fields.ForeignKeyNullableRelation["LocationModel"] = fields.ForeignKeyField(
        "models.LocationModel",
        related_name="events",
        null=True,
        on_delete=fields.SET_NULL,
        description="Optional linked location.",
    )

    # ---------------------------
    # Core fields
    # ---------------------------
    name = fields.CharField(
        max_length=255,
        description="Event title.",
    )
    description = fields.TextField(
        description="Event description.",
    )

    # ---------------------------
    # GEO: PostGIS fields
    # ---------------------------
    point: Point | None = PostGISPointField(
        null=True,
        srid=settings.system.geo_srid,
        description="Center point (lon/lat) for the event.",
    )

    polygon: Polygon | None = PostGISPolygonField(
        null=True,
        srid=settings.system.geo_srid,
        description="Area / polygon for the event.",
    )

    # ---------------------------
    # Links & media
    # ---------------------------
    group_link = fields.CharField(
        max_length=512,
        null=True,
        description="External group/community link.",
    )
    chat_link = fields.CharField(
        max_length=512,
        null=True,
        description="Chat link (e.g. Telegram).",
    )

    image = ImageField(
        directory_name="events",
        field_for_name="name",
    )

    # ---------------------------
    # Schedule relations / data
    # ---------------------------
    schedule_rules: fields.ManyToManyRelation["EventScheduleRuleModel"] = fields.ManyToManyField(
        "models.EventScheduleRuleModel")

    # ---------------------------
    # Mixins: TimestampMixin + WithActiveMixin
    # ---------------------------
    created_at = fields.DatetimeField(
        auto_now_add=True,
        description="Creation timestamp (UTC).",
    )
    updated_at = fields.DatetimeField(
        auto_now=True,
        description="Last update timestamp (UTC).",
    )
    is_active = fields.BooleanField(
        default=True,
        description="Logical active flag.",
    )

    if TYPE_CHECKING:
        account_id: int
        location_id: int | None
        get_image_url: Callable[[], str]
        get_image_webp: Callable[[int, int, str, bool | None], Awaitable[str]]

    class Meta:
        table = "events"
        description = "User events"
