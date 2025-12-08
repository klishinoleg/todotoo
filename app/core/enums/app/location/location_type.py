from functools import lru_cache
from typing import Self

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class LocationType(BaseLabeledEnum):
    POINT = "point"
    AREA = "area"
    PLACE = "place"
    ORGANIZATION = "organization"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.POINT: _("Point"),
            cls.AREA: _("Area"),
            cls.PLACE: _("Place"),
            cls.ORGANIZATION: _("Organization")
        }
