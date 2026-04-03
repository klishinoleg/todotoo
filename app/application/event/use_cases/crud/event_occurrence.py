from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.event.entities.event_occurrence import EventOccurrenceEntity
from domain.event.repositories.event_occurrence import EventOccurrenceFilter


class EventOccurrenceCrudUseCase(BaseCrudUseCase[EventOccurrenceEntity, EventOccurrenceFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(EventOccurrenceEntity, EventOccurrenceFilter, account=account)

