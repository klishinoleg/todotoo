from datetime import datetime
from abc import ABC

from core.enums.app.location.location_type import LocationType
from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.bool_filter import BoolFilterField
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.geometry_filter import GeometryFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.repository import BaseRepository
from domain.location.entities.location import LocationEntity


class LocationFilter[Q](BaseFilter[Q]):
    type: EqualFilterField[LocationType, Q] | None = None
    parent_id: EqualFilterField[int, Q] | None = None
    name: EqualFilterField[str, Q] | None = None
    point: GeometryFilterField[Q] | None = None
    polygon: GeometryFilterField[Q] | None = None
    create_at: RangeFilterField[datetime, Q] | None = None
    is_active: BoolFilterField[Q] | None = None


class LocationRepository[Q](BaseRepository[LocationEntity, LocationFilter[Q]], ABC):
    ...
