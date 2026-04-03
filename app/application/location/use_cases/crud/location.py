from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.location.entities.location import LocationEntity
from domain.location.repositories.location import LocationFilter


class LocationCrudUseCase(BaseCrudUseCase[LocationEntity, LocationFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(LocationEntity, LocationFilter, account=account)

