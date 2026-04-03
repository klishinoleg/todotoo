from application.base.use_case.crud import BaseCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.idea_event.entities.event_comment import IdeaEventCommentEntity
from domain.idea_event.repositories.event import IdeaEventCommentFilter


class IdeaEventCommentCrudUseCase(BaseCrudUseCase[IdeaEventCommentEntity, IdeaEventCommentFilter]):
    def __init__(self, account: AccountEntity | None = None) -> None:
        super().__init__(IdeaEventCommentEntity, IdeaEventCommentFilter, account=account)

