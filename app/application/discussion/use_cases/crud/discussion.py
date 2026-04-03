from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.discussion.entities.discussion import DiscussionEntity
from domain.discussion.repositories.discussion import DiscussionFilter


class DiscussionCrudUseCase(BaseCrudUseCase[DiscussionEntity, DiscussionFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(DiscussionEntity, DiscussionFilter, account=account)

