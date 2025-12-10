from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from application.account.use_cases.auth.auth import AuthUseCase
from core.messages.account.access_control import AccessControlMessages
from domain.account.entities.account import AccountEntity
from domain.base.exceptions import DomainValidationException

# FastAPI bearer scheme
bearer_scheme = HTTPBearer(auto_error=False)
baerer_scheme_with_raise = HTTPBearer(auto_error=True,
                                      scheme_name="Authorization",
                                      description="JWT Bearer access token. Format: Bearer <token>")


def get_auth_use_case() -> AuthUseCase:
    return AuthUseCase()


async def get_current_account(
        credentials: HTTPAuthorizationCredentials = Depends(baerer_scheme_with_raise),
        auth_use_case: AuthUseCase = Depends(get_auth_use_case),
) -> AccountEntity:
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AccessControlMessages.no_credentials_provided(),
        )
    try:
        return await auth_use_case.get_account_by_token(token)
    except DomainValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )


async def get_current_account_or_none(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        auth_use_case: AuthUseCase = Depends(get_auth_use_case)
) -> AccountEntity | None:
    token = credentials.credentials if credentials else None
    if not token:
        return None
    try:
        return await auth_use_case.get_account_by_token(token)
    except DomainValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )


def get_account_func(with_raise: bool = False) -> Callable:
    if with_raise:
        return get_current_account
    return get_current_account_or_none
