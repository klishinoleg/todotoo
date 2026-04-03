from dataclasses import dataclass, field
from datetime import datetime

from core.enums.app.idea_participant.idea_role import IdeaRoleEnum
from core.enums.app.idea_participant.participant_status import ParticipantStatusEnum
from core.helpers.func.date_time import get_utc_time
from domain.base.entity import BaseEntity


@dataclass(slots=True, kw_only=True)
class IdeaParticipantEntity(BaseEntity):
    idea_id: int
    account_id: int
    role: IdeaRoleEnum = IdeaRoleEnum.VIEWER
    status: ParticipantStatusEnum = ParticipantStatusEnum.PENDING
    joined_at: datetime = field(default_factory=get_utc_time)
    invited_by: int | None = None

