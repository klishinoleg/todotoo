from abc import ABC
from datetime import datetime

from domain.base.filters.base_filter import BaseFilter
from domain.base.filters.equal_filter import EqualFilterField
from domain.base.filters.range_filter import RangeFilterField
from domain.base.repository import BaseRepository
from domain.idea_participant.entities.idea_participant import IdeaParticipantEntity
from domain.idea_participant.entities.participation_request import ParticipationRequestEntity


class IdeaParticipantFilter[Q](BaseFilter[Q]):
    idea_id: EqualFilterField[int, Q] | None = None
    account_id: EqualFilterField[int, Q] | None = None
    role: EqualFilterField[str, Q] | None = None
    status: EqualFilterField[str, Q] | None = None
    joined_at: RangeFilterField[datetime, Q] | None = None


class IdeaParticipantRepository[Q](BaseRepository[IdeaParticipantEntity, IdeaParticipantFilter[Q]], ABC):
    ...


class ParticipationRequestFilter[Q](BaseFilter[Q]):
    idea_id: EqualFilterField[int, Q] | None = None
    account_id: EqualFilterField[int, Q] | None = None
    reviewed_by: EqualFilterField[int, Q] | None = None
    status: EqualFilterField[str, Q] | None = None


class ParticipationRequestRepository[Q](BaseRepository[ParticipationRequestEntity, ParticipationRequestFilter[Q]], ABC):
    ...
