from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.discussion.entities.discussion_message import DiscussionMessageEntity
from domain.discussion.repositories.discussion import DiscussionMessageFilter


class DiscussionMessageCrudUseCase(BaseCrudUseCase[DiscussionMessageEntity, DiscussionMessageFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(DiscussionMessageEntity, DiscussionMessageFilter, account=account)

