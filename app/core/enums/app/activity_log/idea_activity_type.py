from functools import lru_cache

from core.enums.base import BaseLabeledEnum
from core.i18n import _


class IdeaActivityTypeEnum(BaseLabeledEnum):
    IDEA_CREATED = "idea_created"
    PARTICIPANT_JOINED = "participant_joined"
    PARTICIPANT_LEFT = "participant_left"
    REQUEST_CREATED = "request_created"
    REQUEST_APPROVED = "request_approved"
    ROLE_CHANGED = "role_changed"
    PLAN_CREATED = "plan_created"
    STEP_COMPLETED = "step_completed"
    MEETING_CREATED = "meeting_created"
    EVENT_CREATED = "event_created"

    @classmethod
    @lru_cache(maxsize=1)
    def _label_map(cls) -> dict[str, str]:
        return {
            cls.IDEA_CREATED: _("Idea created"),
            cls.PARTICIPANT_JOINED: _("Participant joined"),
            cls.PARTICIPANT_LEFT: _("Participant left"),
            cls.REQUEST_CREATED: _("Request created"),
            cls.REQUEST_APPROVED: _("Request approved"),
            cls.ROLE_CHANGED: _("Role changed"),
            cls.PLAN_CREATED: _("Plan created"),
            cls.STEP_COMPLETED: _("Step completed"),
            cls.MEETING_CREATED: _("Meeting created"),
            cls.EVENT_CREATED: _("Event created"),
        }

