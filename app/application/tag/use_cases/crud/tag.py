from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.tag.entities.tag import TagEntity
from domain.tag.repositories.tag import TagFilter


class TagCrudUseCase(BaseCrudUseCase[TagEntity, TagFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(TagEntity, TagFilter, account=account)

