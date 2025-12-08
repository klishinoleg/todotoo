from __future__ import annotations
from abc import ABC
from domain.base.filters.base_filter import BaseFilterField
from domain.base.value_objects.geometry import (GeometryPolygon, GeometryPoint)


# Allowed shapes for "contains"


class GeometryFilterField[Q](BaseFilterField[Q], ABC):
    """
    Universal geometry filter.

    contains:
        object must be inside circle/polygon.

    exclude:
        object must be outside circle/polygon.

    point + distance_meters:
        distance from given point.

    Repository must implement:
        - filter_geometry_contains(shape)
        - filter_geometry_exclude(shape)
        - filter_within_distance(point, meters)
    """

    contains: GeometryPolygon | None = None
    exclude: GeometryPolygon | None = None
    point: GeometryPoint | None = None
    distance_meters: float | None = None
