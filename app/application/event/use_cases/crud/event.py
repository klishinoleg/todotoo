from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.event.entities.event import EventEntity
from domain.event.repositories.event import EventFilter


class EventCrudUseCase(BaseCrudUseCase[EventEntity, EventFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(EventEntity, EventFilter, account=account)

