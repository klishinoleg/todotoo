from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class PlanStepStatusEnum(BaseLabeledEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    SKIPPED = "skipped"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.TODO: _("Todo"),
            cls.IN_PROGRESS: _("In progress"),
            cls.DONE: _("Done"),
            cls.SKIPPED: _("Skipped"),
        }

