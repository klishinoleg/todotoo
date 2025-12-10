from tortoise.queryset import QuerySet

from core.di.repository import DIRepository
from core.enums.di.repository import RepositoryType, FilterFieldType
from domain.base.filters.geometry_filter import GeometryFilterField
from domain.base.value_objects.geometry import GeometryPolygon, GeometryPoint
from infrastructure.repository.tortoise.base.geo.convert import (
    to_postgis_polygon,
    to_postgis_point,
)


class TortoiseGeometryFilterField(GeometryFilterField[QuerySet]):

    def extend_query(self, name: str, query: QuerySet) -> QuerySet:

        # contains polygon → ST_Within
        if self.contains:
            return self._filter_contains(query, name, self.contains)

        # exclude polygon → NOT ST_Within
        if self.exclude:
            return self._filter_exclude(query, name, self.exclude)

        # distance search → ST_DWithin
        if self.point and self.distance_meters:
            return self._filter_distance(query, name, self.point, self.distance_meters)

        return query

    # ----------------------------------------------------------------------

    @staticmethod
    def _filter_contains(query: QuerySet, field: str, polygon: GeometryPolygon) -> QuerySet:
        pg_polygon = to_postgis_polygon(polygon)

        return query.filter(
            **{
                f"{field}__geo_within": pg_polygon
            }
        )

    @staticmethod
    def _filter_exclude(query: QuerySet, field: str, polygon: GeometryPolygon) -> QuerySet:
        pg_polygon = to_postgis_polygon(polygon)

        return query.exclude(
            **{
                f"{field}__geo_within": pg_polygon
            }
        )

    @staticmethod
    def _filter_distance(query: QuerySet, field: str, point: GeometryPoint, meters: float) -> QuerySet:
        pg_point = to_postgis_point(point)

        return query.filter(
            **{
                f"{field}__distance_lte": (pg_point, meters)
            }
        )


DIRepository.register_filter(FilterFieldType.GEOMETRY, TortoiseGeometryFilterField, RepositoryType.TORTOISE)
