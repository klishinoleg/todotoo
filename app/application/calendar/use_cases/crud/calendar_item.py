from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.calendar.entities.calendar_item import CalendarItemEntity
from domain.calendar.repositories.calendar_item import CalendarItemFilter


class CalendarItemCrudUseCase(BaseCrudUseCase[CalendarItemEntity, CalendarItemFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(CalendarItemEntity, CalendarItemFilter, account=account)

