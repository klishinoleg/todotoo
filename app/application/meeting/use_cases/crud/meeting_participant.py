from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.meeting.entities.meeting_participant import MeetingParticipantEntity
from domain.meeting.repositories.meeting import MeetingParticipantFilter


class MeetingParticipantCrudUseCase(BaseCrudUseCase[MeetingParticipantEntity, MeetingParticipantFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(MeetingParticipantEntity, MeetingParticipantFilter, account=account)

