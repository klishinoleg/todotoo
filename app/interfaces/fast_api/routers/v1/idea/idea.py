import secrets
from datetime import timedelta
from typing import Any

from fastapi import Depends, HTTPException, Query, status
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError

from application.idea.use_cases.crud.idea import IdeaCrudUseCase
from application.idea.use_cases.guard import ensure_idea_admin
from core.config.settings import settings
from core.di.email import DIEmailSenderProvider
from core.enums.app.activity_log.idea_activity_type import IdeaActivityTypeEnum
from core.enums.app.idea_participant.participant_status import ParticipantStatusEnum
from core.helpers.func.date_time import get_utc_time
from domain.account.entities.account import AccountEntity
from domain.base.exceptions import DomainValidationException
from interfaces.fast_api.deps.account import get_current_account
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter
from infrastructure.repository.tortoise.models.activity_log.idea_activity import IdeaActivityModel
from infrastructure.repository.tortoise.models.idea.idea import IdeaModel
from infrastructure.repository.tortoise.models.idea_invite.idea_invite import IdeaInviteModel
from infrastructure.repository.tortoise.models.idea_participant.idea_participant import IdeaParticipantModel


class IdeaInviteCreateDTO(BaseModel):
    email: str
    role: str = "contributor"
    message: str | None = None


class IdeaInviteCreateResponseDTO(BaseModel):
    id: int
    idea_id: int
    email: str
    role: str
    token: str
    email_sent: bool
    expires_at: str


class IdeaSelfResponseDTO(BaseModel):
    idea_id: int
    account_id: int
    role: str | None = None
    status: str | None = None
    is_participant: bool = False


class IdeaMembershipActionResponseDTO(BaseModel):
    success: bool
    idea_id: int
    account_id: int
    role: str | None = None
    status: str | None = None


class AcceptInviteResponseDTO(BaseModel):
    success: bool
    idea_id: int
    account_id: int
    role: str
    status: str


class IdeaListItemDTO(BaseModel):
    id: int
    title: str
    description: str
    slogan: str | None = None
    cover_image: str | None = None
    creator_id: int
    visibility: str
    status: str
    is_active: bool
    created_at: str
    updated_at: str


class IdeaListResponseDTO(BaseModel):
    items: list[dict[str, Any]]
    total: int
    page: int
    per_page: int


def _require_account_id(account: AccountEntity) -> int:
    if account.id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return account.id


async def _send_idea_invite_email(
        *,
        to_email: str,
        invite_token: str,
        idea_id: int,
        role: str,
        message: str | None,
) -> bool:
    web_app_url = settings.system.web_app_url.strip().rstrip("/")
    invite_link = f"{web_app_url}/invite/{invite_token}" if web_app_url else invite_token
    subject = f"Invitation to idea #{idea_id}"
    text_lines = [
        f"You are invited to idea #{idea_id}.",
        f"Role: {role}",
        f"Invite link: {invite_link}",
    ]
    if message:
        text_lines.append(f"Message: {message}")
    text_body = "\n".join(text_lines)

    try:
        sender = DIEmailSenderProvider.get()
        await sender.send_email(to_email=to_email, subject=subject, text_body=text_body)
        return True
    except Exception:
        return False


class IdeaRouter(V1CrudRouter[IdeaCrudUseCase]):
    prefix = "/ideas"
    tags = ["v1/idea"]
    use_case_cls = IdeaCrudUseCase

    def register_custom_routes(self) -> None:
        router = self.router

        @router.get("/my/", response_model=IdeaListResponseDTO)
        async def list_my_ideas(
                page: int = Query(default=1, ge=1),
                per_page: int = Query(default=20, ge=1, le=100),
                account: AccountEntity = Depends(get_current_account),
        ) -> IdeaListResponseDTO:
            account_id = _require_account_id(account)
            query = IdeaModel.filter(creator_id=account_id).order_by("-updated_at")
            total = await query.count()
            offset = (page - 1) * per_page
            models = await query.offset(offset).limit(per_page)
            items = [self._serialize_idea_model(model) for model in models]
            return IdeaListResponseDTO(items=items, total=total, page=page, per_page=per_page)

        @router.get("/participating/", response_model=IdeaListResponseDTO)
        async def list_participating_ideas(
                page: int = Query(default=1, ge=1),
                per_page: int = Query(default=20, ge=1, le=100),
                account: AccountEntity = Depends(get_current_account),
        ) -> IdeaListResponseDTO:
            account_id = _require_account_id(account)
            participant_query = IdeaParticipantModel.filter(
                account_id=account_id,
                status=str(ParticipantStatusEnum.ACTIVE),
            ).order_by("-joined_at")
            idea_ids = await participant_query.values_list("idea_id", flat=True)
            if not idea_ids:
                return IdeaListResponseDTO(items=[], total=0, page=page, per_page=per_page)

            query = IdeaModel.filter(id__in=list(idea_ids)).order_by("-updated_at")
            total = await query.count()
            offset = (page - 1) * per_page
            models = await query.offset(offset).limit(per_page)
            items = [self._serialize_idea_model(model) for model in models]
            return IdeaListResponseDTO(items=items, total=total, page=page, per_page=per_page)

        @router.get("/{idea_id}/me/", response_model=IdeaSelfResponseDTO)
        async def get_my_membership(
                idea_id: int,
                account: AccountEntity = Depends(get_current_account),
        ) -> IdeaSelfResponseDTO:
            account_id = _require_account_id(account)
            participant = await IdeaParticipantModel.filter(idea_id=idea_id, account_id=account_id).first()
            if participant is None:
                return IdeaSelfResponseDTO(
                    idea_id=idea_id,
                    account_id=account_id,
                    is_participant=False,
                )
            return IdeaSelfResponseDTO(
                idea_id=idea_id,
                account_id=account_id,
                role=participant.role,
                status=participant.status,
                is_participant=True,
            )

        @router.post("/{idea_id}/join/", response_model=IdeaMembershipActionResponseDTO)
        async def join_idea(
                idea_id: int,
                account: AccountEntity = Depends(get_current_account),
        ) -> IdeaMembershipActionResponseDTO:
            account_id = _require_account_id(account)
            idea = await IdeaModel.filter(id=idea_id).first()
            if idea is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Idea not found")

            participant = await IdeaParticipantModel.filter(idea_id=idea_id, account_id=account_id).first()
            if participant is None:
                participant = await IdeaParticipantModel.create(
                    idea_id=idea_id,
                    account_id=account_id,
                    role="viewer",
                    status=str(ParticipantStatusEnum.ACTIVE),
                    invited_by=None,
                )
            else:
                participant.status = str(ParticipantStatusEnum.ACTIVE)
                await participant.save(update_fields=["status"])

            await IdeaActivityModel.create(
                idea_id=idea_id,
                account_id=account_id,
                type=str(IdeaActivityTypeEnum.PARTICIPANT_JOINED),
                payload={},
            )
            return IdeaMembershipActionResponseDTO(
                success=True,
                idea_id=idea_id,
                account_id=account_id,
                role=participant.role,
                status=participant.status,
            )

        @router.post("/{idea_id}/leave/", response_model=IdeaMembershipActionResponseDTO)
        async def leave_idea(
                idea_id: int,
                account: AccountEntity = Depends(get_current_account),
        ) -> IdeaMembershipActionResponseDTO:
            account_id = _require_account_id(account)
            participant = await IdeaParticipantModel.filter(idea_id=idea_id, account_id=account_id).first()
            if participant is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Participant not found")

            participant.status = str(ParticipantStatusEnum.DECLINED)
            await participant.save(update_fields=["status"])
            await IdeaActivityModel.create(
                idea_id=idea_id,
                account_id=account_id,
                type=str(IdeaActivityTypeEnum.PARTICIPANT_LEFT),
                payload={},
            )
            return IdeaMembershipActionResponseDTO(
                success=True,
                idea_id=idea_id,
                account_id=account_id,
                role=participant.role,
                status=participant.status,
            )

        @router.post("/{idea_id}/invites/", response_model=IdeaInviteCreateResponseDTO, status_code=status.HTTP_201_CREATED)
        async def create_invite(
                idea_id: int,
                data: IdeaInviteCreateDTO,
                account: AccountEntity = Depends(get_current_account),
        ) -> IdeaInviteCreateResponseDTO:
            try:
                await ensure_idea_admin(account, idea_id)
            except DomainValidationException as exc:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)

            account_id = _require_account_id(account)
            expires_at = get_utc_time() + timedelta(days=7)
            token = secrets.token_urlsafe(24)
            try:
                invite = await IdeaInviteModel.create(
                    idea_id=idea_id,
                    email=data.email.strip().lower(),
                    role=data.role,
                    message=data.message,
                    token=token,
                    status="pending",
                    created_by=account_id,
                    expires_at=expires_at,
                )
            except IntegrityError:
                token = secrets.token_urlsafe(32)
                invite = await IdeaInviteModel.create(
                    idea_id=idea_id,
                    email=data.email.strip().lower(),
                    role=data.role,
                    message=data.message,
                    token=token,
                    status="pending",
                    created_by=account_id,
                    expires_at=expires_at,
                )

            email_sent = await _send_idea_invite_email(
                to_email=invite.email,
                invite_token=invite.token,
                idea_id=invite.idea_id,
                role=invite.role,
                message=invite.message,
            )
            return IdeaInviteCreateResponseDTO(
                id=invite.id,
                idea_id=invite.idea_id,
                email=invite.email,
                role=invite.role,
                token=invite.token,
                email_sent=email_sent,
                expires_at=invite.expires_at.isoformat(),
            )

        @router.post("/invites/{invite_token}/accept/", response_model=AcceptInviteResponseDTO)
        async def accept_invite(
                invite_token: str,
                account: AccountEntity = Depends(get_current_account),
        ) -> AcceptInviteResponseDTO:
            account_id = _require_account_id(account)
            invite = await IdeaInviteModel.filter(token=invite_token, status="pending").first()
            if invite is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
            if invite.expires_at < get_utc_time():
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invite is expired")

            participant = await IdeaParticipantModel.filter(idea_id=invite.idea_id, account_id=account_id).first()
            if participant is None:
                participant = await IdeaParticipantModel.create(
                    idea_id=invite.idea_id,
                    account_id=account_id,
                    role=invite.role,
                    status=str(ParticipantStatusEnum.ACTIVE),
                    invited_by=invite.created_by,
                )
            else:
                participant.role = invite.role
                participant.status = str(ParticipantStatusEnum.ACTIVE)
                participant.invited_by = invite.created_by
                await participant.save(update_fields=["role", "status", "invited_by"])

            invite.status = "accepted"
            invite.accepted_by = account_id
            invite.accepted_at = get_utc_time()
            await invite.save(update_fields=["status", "accepted_by", "accepted_at"])

            await IdeaActivityModel.create(
                idea_id=invite.idea_id,
                account_id=account_id,
                type=str(IdeaActivityTypeEnum.PARTICIPANT_JOINED),
                payload={"source": "invite", "invite_id": invite.id},
            )
            return AcceptInviteResponseDTO(
                success=True,
                idea_id=invite.idea_id,
                account_id=account_id,
                role=participant.role,
                status=participant.status,
            )

    @staticmethod
    def _serialize_idea_model(model: IdeaModel) -> dict[str, Any]:
        return {
            "id": model.id,
            "title": model.title,
            "description": model.description,
            "slogan": model.slogan,
            "cover_image": model.cover_image,
            "creator_id": model.creator_id,
            "visibility": model.visibility,
            "status": model.status,
            "is_active": model.is_active,
            "created_at": model.created_at.isoformat(),
            "updated_at": model.updated_at.isoformat(),
        }


idea_crud_router = IdeaRouter()
router = idea_crud_router.router
