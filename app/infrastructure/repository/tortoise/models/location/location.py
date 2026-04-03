from __future__ import annotations

from typing import TYPE_CHECKING

from postgis import Polygon, Point
from tortoise import fields

from core.config.settings import settings
from core.enums.app.location.location_type import LocationType
from infrastructure.repository.tortoise.base.fields.point import PostGISPointField
from infrastructure.repository.tortoise.base.fields.polygon import PostGISPolygonField
from infrastructure.repository.tortoise.base.model import BaseTortoiseModel


class LocationModel(BaseTortoiseModel):
    """
    Tortoise ORM model for LocationEntity.

    Contains:
        - PostGIS point for quick distance queries
        - Generic PostGIS geometry for polygons/areas
    """

    # ---------------------------
    # Core fields
    # ---------------------------
    name = fields.CharField(
        max_length=255,
        description="Human-readable location name.",
    )

    type: LocationType = fields.CharEnumField(
        LocationType,
        description="Location type (point, area, place, organization, etc.).",
    )

    # ---------------------------
    # GEO: PostGIS fields
    # ---------------------------
    point: Point | None = PostGISPointField(
        null=True,
        srid=settings.system.geo_srid,
        description="Center point (lon/lat) for the location.",
    )

    polygon: Polygon | None = PostGISPolygonField(
        null=True,
        srid=settings.system.geo_srid,
        description="Full geometry (polygon, etc.) for the location.",
    )

    # ---------------------------
    # Address
    # ---------------------------
    address_raw = fields.TextField(
        null=True,
        description="Raw unformatted address from provider (e.g. Google).",
    )

    address_structured: dict = fields.JSONField(
        null=True,
        description="Structured address dict (country, city, street, etc.).",
    )

    # ---------------------------
    # Hierarchy & media
    # ---------------------------
    parent: fields.ForeignKeyNullableRelation["LocationModel"] = fields.ForeignKeyField(
        "models.LocationModel",
        related_name="children",
        null=True,
        on_delete=fields.SET_NULL,
        description="Parent location for hierarchical structure.",
    )

    image = fields.CharField(max_length=1024, null=True)

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
        parent_id: int | None

    class Meta:
        table = "locations"
        description = "Geographic locations (points and areas)"
