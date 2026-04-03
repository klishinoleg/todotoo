from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.event.entities.event_schedule_rule import EventScheduleRuleEntity
from domain.event.repositories.event_schedule_rule import EventScheduleRuleFilter


class EventScheduleRuleCrudUseCase(BaseCrudUseCase[EventScheduleRuleEntity, EventScheduleRuleFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(EventScheduleRuleEntity, EventScheduleRuleFilter, account=account)

