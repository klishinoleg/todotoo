from dataclasses import dataclass
from datetime import datetime

from core.enums.app.idea_participant.request_status import RequestStatusEnum
from domain.base.entity import BaseEntity
from domain.base.mixins.timestamp import TimestampMixin


@dataclass(slots=True, kw_only=True)
class ParticipationRequestEntity(BaseEntity, TimestampMixin):
    idea_id: int
    account_id: int
    message: str | None = None
    status: RequestStatusEnum = RequestStatusEnum.PENDING
    reviewed_by: int | None = None
    reviewed_at: datetime | None = None

