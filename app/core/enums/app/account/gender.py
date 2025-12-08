from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class Gender(BaseLabeledEnum):
    MALE = "male"
    FEMALE = "female"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.MALE: _("Male"),
            cls.FEMALE: _("Female"),
        }
