from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.event.entities.event_occurrence_message import EventOccurrenceMessageEntity
from domain.event.repositories.event_occurrence_message import EventOccurrenceMessageFilter


class EventOccurrenceMessageCrudUseCase(BaseCrudUseCase[EventOccurrenceMessageEntity, EventOccurrenceMessageFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(EventOccurrenceMessageEntity, EventOccurrenceMessageFilter, account=account)

