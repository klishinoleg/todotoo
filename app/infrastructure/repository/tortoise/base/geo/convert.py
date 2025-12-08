from postgis import Point, Polygon
from core.config.settings import settings

from domain.base.value_objects.geometry import GeometryPoint, GeometryPolygon


# ----------------------------
#  Domain → PostGIS
# ----------------------------

def to_postgis_point(point: GeometryPoint | None) -> Point | None:
    if point is None:
        return None
    return Point(point.longitude, point.latitude, srid=settings.system.geo_srid)


def to_postgis_polygon(polygon: GeometryPolygon | None) -> Polygon | None:
    if polygon is None:
        return None
    return Polygon(polygon.points, srid=settings.system.geo_srid)


# ----------------------------
#  PostGIS → Domain
# ----------------------------

def from_postgis_point(pg: Point | None) -> GeometryPoint | None:
    """
    Convert PostGIS Point into domain GeometryPoint.
    PostGIS point stores coordinates as (x=lng, y=lat).
    """
    if pg is None:
        return None
    return GeometryPoint(
        latitude=pg.y,
        longitude=pg.x,
    )


def from_postgis_polygon(pg: Polygon | None) -> GeometryPolygon | None:
    """
    Convert PostGIS Polygon into domain GeometryPolygon.
    Polygon.points is a list of (x, y) tuples with lng, lat order.
    """
    if pg is None:
        return None
    return GeometryPolygon(points=pg.coords)
