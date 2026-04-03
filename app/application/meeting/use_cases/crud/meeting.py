from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.meeting.entities.meeting import MeetingEntity
from domain.meeting.repositories.meeting import MeetingFilter


class MeetingCrudUseCase(BaseCrudUseCase[MeetingEntity, MeetingFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(MeetingEntity, MeetingFilter, account=account)

