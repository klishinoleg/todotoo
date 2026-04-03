from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.event.entities.event_member import EventMemberEntity
from domain.event.repositories.event_member import EventMemberFilter


class EventMemberCrudUseCase(BaseCrudUseCase[EventMemberEntity, EventMemberFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(EventMemberEntity, EventMemberFilter, account=account)

