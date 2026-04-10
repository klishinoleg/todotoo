from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from application.idea.use_cases.guard import ensure_idea_participant
from application.motivation.use_cases.crud.motivator import MotivatorCrudUseCase
from domain.account.entities.account import AccountEntity
from domain.base.exceptions import DomainValidationException
from interfaces.fast_api.deps.account import get_current_account
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter
from infrastructure.repository.tortoise.models.discussion.discussion import DiscussionModel
from infrastructure.repository.tortoise.models.motivation.motivator import MotivatorModel


class MotivatorDiscussionResponseDTO(BaseModel):
    motivator_id: int
    discussion_id: int | None = None
    idea_id: int | None = None


class MotivatorRouter(V1CrudRouter[MotivatorCrudUseCase]):
    prefix = "/motivators"
    tags = ["v1/motivation"]
    use_case_cls = MotivatorCrudUseCase

    def register_custom_routes(self) -> None:
        router = self.router

        @router.get("/{motivator_id}/discussion/", response_model=MotivatorDiscussionResponseDTO)
        async def get_motivator_discussion(
                motivator_id: int,
                account: AccountEntity = Depends(get_current_account),
        ) -> MotivatorDiscussionResponseDTO:
            motivator = await MotivatorModel.filter(id=motivator_id).first()
            if motivator is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motivator not found")
            try:
                await ensure_idea_participant(account, motivator.idea_id)
            except DomainValidationException as exc:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)

            discussion = await DiscussionModel.filter(
                idea_id=motivator.idea_id,
                context_type="motivator",
                context_id=motivator_id,
            ).first()
            return MotivatorDiscussionResponseDTO(
                motivator_id=motivator_id,
                discussion_id=discussion.id if discussion else None,
                idea_id=motivator.idea_id,
            )

        @router.post("/{motivator_id}/discussion/", response_model=MotivatorDiscussionResponseDTO)
        async def create_motivator_discussion(
                motivator_id: int,
                account: AccountEntity = Depends(get_current_account),
        ) -> MotivatorDiscussionResponseDTO:
            if account.id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
            motivator = await MotivatorModel.filter(id=motivator_id).first()
            if motivator is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motivator not found")
            try:
                await ensure_idea_participant(account, motivator.idea_id)
            except DomainValidationException as exc:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)

            discussion = await DiscussionModel.filter(
                idea_id=motivator.idea_id,
                context_type="motivator",
                context_id=motivator_id,
            ).first()
            if discussion is None:
                discussion = await DiscussionModel.create(
                    idea_id=motivator.idea_id,
                    title=f"Motivator #{motivator_id}",
                    created_by=account.id,
                    context_type="motivator",
                    context_id=motivator_id,
                )

            return MotivatorDiscussionResponseDTO(
                motivator_id=motivator_id,
                discussion_id=discussion.id,
                idea_id=motivator.idea_id,
            )


motivator_crud_router = MotivatorRouter()
router = motivator_crud_router.router
