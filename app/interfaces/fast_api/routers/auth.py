from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from application.account.dto.account import AccountDTO
from application.account.dto.account_auth_profile import AccountAuthProfileDTO
from application.account.dto.auth.oauth_flow import OAuthAuthorizeUrlDTO, OAuthCallbackDTO
from application.account.dto.auth.profile_management import (
    AuthProfileLinkConfirmRequestDTO,
    AuthProfileOAuthCallbackLinkRequestDTO,
    AuthPasswordProfileLinkRequestDTO,
    AuthProfileDeleteResponseDTO,
    AuthProfileLinkRequestDTO,
    AuthProfileLinkResponseDTO,
)
from application.account.dto.auth.request.oauth import AuthRequestOAuthDTO
from application.account.dto.auth.request.oauth import AuthRequestOAuthLoginDTO, AuthRequestOAuthSignUpDTO
from application.account.dto.auth.request.oauth import OAuthProviderDataDTO
from application.account.dto.auth.response import AuthResponseDTO
from application.account.services.oauth_flow import OAuthFlowService
from core.enums.app.account.auth_provider import AuthActionType, AuthProviderType
from core.enums.system.logger.message_levels import LogMessageLevel
from core.logger.logger import Logger
from domain.account.entities.account import AccountEntity
from domain.base.exceptions import DomainValidationException
from interfaces.fast_api.deps.account import get_current_account
from application.account.use_cases.auth.auth import AuthUseCase, AuthRequestTelegramDTO, AuthRequestSignUpDTO, \
    AuthRequestLoginDTO
from application.account.use_cases.auth.profile_management import AuthProfileManagementUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/telegram/", response_model=AuthResponseDTO)
async def auth_via_telegram(dto: AuthRequestTelegramDTO) -> AuthResponseDTO:
    try:
        return await AuthUseCase().telegram(dto)
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.get("/me/", response_model=AccountDTO)
async def get_me(account: AccountEntity = Depends(get_current_account)) -> AccountDTO:
    return await AuthUseCase().me(account)


@router.get("/profiles/", response_model=list[AccountAuthProfileDTO])
async def get_profiles(
        account: AccountEntity = Depends(get_current_account)
) -> list[AccountAuthProfileDTO]:
    try:
        return await AuthProfileManagementUseCase().list_profiles(account)
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/profiles/link/", response_model=AuthProfileLinkResponseDTO)
async def link_auth_profile(
        data: AuthProfileLinkRequestDTO,
        account: AccountEntity = Depends(get_current_account),
) -> AuthProfileLinkResponseDTO:
    try:
        return await AuthProfileManagementUseCase().link_profile(
            account=account,
            provider_type=data.provider_type,
            provider_raw_data=data.provider_data,
            confirm_merge=data.confirm_merge,
        )
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/profiles/link/password/", response_model=AuthProfileLinkResponseDTO)
async def link_password_profile(
        data: AuthPasswordProfileLinkRequestDTO,
        account: AccountEntity = Depends(get_current_account),
) -> AuthProfileLinkResponseDTO:
    try:
        provider_raw_data = {
            "email": data.email,
            "password": data.password,
            "confirm_password": data.confirm_password,
            "public_name": data.public_name,
            "language_code": data.language_code,
        }
        return await AuthProfileManagementUseCase().link_profile(
            account=account,
            provider_type=AuthProviderType.PASSWORD,
            provider_raw_data=provider_raw_data,
            confirm_merge=data.confirm_merge,
        )
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/profiles/link/confirm/", response_model=AuthProfileLinkResponseDTO)
async def confirm_link_auth_profile(
        data: AuthProfileLinkConfirmRequestDTO,
        account: AccountEntity = Depends(get_current_account),
) -> AuthProfileLinkResponseDTO:
    try:
        return await AuthProfileManagementUseCase().confirm_link_merge(
            account=account,
            operation_code=data.operation_code,
        )
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.delete("/profiles/{profile_id}/", response_model=AuthProfileDeleteResponseDTO)
async def delete_profile(
        profile_id: int,
        account: AccountEntity = Depends(get_current_account),
) -> AuthProfileDeleteResponseDTO:
    try:
        return await AuthProfileManagementUseCase().delete_profile(account, profile_id)
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/profiles/link/oauth/{provider_type}/callback/", response_model=AuthProfileLinkResponseDTO)
async def link_oauth_profile_callback(
        provider_type: AuthProviderType,
        data: AuthProfileOAuthCallbackLinkRequestDTO,
        account: AccountEntity = Depends(get_current_account),
) -> AuthProfileLinkResponseDTO:
    service = OAuthFlowService()
    try:
        Logger.auth(
            "api.auth.profile.link.oauth.callback.start",
            provider_type=str(provider_type),
            account_id=account.id,
            has_state=bool(data.state),
            has_redirect_uri=bool(data.redirect_uri),
            has_action_type=bool(data.action_type),
            has_user=bool(data.user),
            confirm_merge=data.confirm_merge,
        )
        if data.state:
            service.resolve_action_type(provider_type, data.state, data.action_type)
        provider_data = await service.exchange_code_for_provider_data(
            provider_type=provider_type,
            code=data.code,
            redirect_uri=data.redirect_uri,
            user=data.user,
        )
        provider_data_dto = OAuthProviderDataDTO.model_validate(provider_data)
        Logger.auth(
            "api.auth.profile.link.oauth.callback.provider_data.ready",
            provider_type=str(provider_type),
            account_id=account.id,
            has_provider_user_id=bool(provider_data_dto.provider_user_id),
            has_email=bool(provider_data_dto.email),
        )
        result = await AuthProfileManagementUseCase().link_profile(
            account=account,
            provider_type=provider_type,
            provider_raw_data=provider_data,
            confirm_merge=data.confirm_merge,
        )
        Logger.auth(
            "api.auth.profile.link.oauth.callback.success",
            provider_type=str(provider_type),
            account_id=account.id,
            status=result.status,
            profile_id=result.profile.id if result.profile else None,
            operation_code=result.operation_code,
            merged_account_id=result.merged_account_id,
            merged_account_deleted=result.merged_account_deleted,
        )
        return result
    except DomainValidationException as exc:
        Logger.auth(
            "api.auth.profile.link.oauth.callback.error",
            level=LogMessageLevel.WARN,
            provider_type=str(provider_type),
            account_id=account.id,
            detail=exc.message,
        )
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(account: AccountEntity = Depends(get_current_account)) -> Response:
    try:
        await AuthUseCase().logout(account)
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/signup/", response_model=AuthResponseDTO)
async def signup(data: AuthRequestSignUpDTO) -> AuthResponseDTO:
    try:
        return await AuthUseCase().register(data)
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/oauth/signup/", response_model=AuthResponseDTO)
async def oauth_signup(data: AuthRequestOAuthSignUpDTO) -> AuthResponseDTO:
    try:
        return await AuthUseCase().register(data)
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/login/", response_model=AuthResponseDTO)
async def login(data: AuthRequestLoginDTO) -> AuthResponseDTO:
    try:
        return await AuthUseCase().login(data)
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/oauth/", response_model=AuthResponseDTO)
async def oauth(data: AuthRequestOAuthDTO) -> AuthResponseDTO:
    try:
        Logger.auth(
            "api.auth.oauth.start",
            provider_type=str(data.provider_type),
        )
        return await AuthUseCase().oauth_auth(data)
    except DomainValidationException as exc:
        Logger.auth(
            "api.auth.oauth.error",
            level=LogMessageLevel.WARN,
            provider_type=str(data.provider_type),
            detail=exc.message,
        )
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/oauth/login/", response_model=AuthResponseDTO)
async def oauth_login(data: AuthRequestOAuthLoginDTO) -> AuthResponseDTO:
    try:
        return await AuthUseCase().oauth_auth(
            AuthRequestOAuthDTO(
                provider_type=data.provider_type,
                provider_data=data.provider_data,
            )
        )
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.get("/oauth/{provider_type}/url/", response_model=OAuthAuthorizeUrlDTO)
async def oauth_authorize_url(
        provider_type: AuthProviderType,
        action_type: AuthActionType = AuthActionType.LOGIN,
        redirect_uri: str | None = None,
) -> OAuthAuthorizeUrlDTO:
    try:
        return OAuthFlowService().build_authorize_url(provider_type, action_type, redirect_uri)
    except DomainValidationException as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)


@router.post("/oauth/{provider_type}/callback/", response_model=AuthResponseDTO)
async def oauth_callback(
        provider_type: AuthProviderType,
        data: OAuthCallbackDTO,
) -> AuthResponseDTO:
    service = OAuthFlowService()
    try:
        Logger.auth(
            "api.auth.oauth.callback.start",
            provider_type=str(provider_type),
            has_state=bool(data.state),
            has_redirect_uri=bool(data.redirect_uri),
            has_action_type=bool(data.action_type),
            has_user=bool(data.user),
        )
        if data.state:
            service.resolve_action_type(provider_type, data.state, data.action_type)
        provider_data = await service.exchange_code_for_provider_data(
            provider_type=provider_type,
            code=data.code,
            redirect_uri=data.redirect_uri,
            user=data.user,
        )
        provider_data_dto = OAuthProviderDataDTO.model_validate(provider_data)
        Logger.auth(
            "api.auth.oauth.callback.provider_data.ready",
            provider_type=str(provider_type),
            has_provider_user_id=bool(provider_data_dto.provider_user_id),
            has_email=bool(provider_data_dto.email),
        )
        return await AuthUseCase().oauth_auth(
            AuthRequestOAuthDTO(
                provider_type=provider_type,
                provider_data=provider_data_dto,
            )
        )
    except DomainValidationException as exc:
        Logger.auth(
            "api.auth.oauth.callback.error",
            level=LogMessageLevel.WARN,
            provider_type=str(provider_type),
            detail=exc.message,
        )
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.message)
