from fastapi import APIRouter, Depends

from application.account.dto.account import AccountDTO
from application.account.dto.account_auth_profile import AccountAuthProfileDTO
from application.account.dto.auth.response import AuthResponseDTO
from domain.account.entities.account import AccountEntity
from interfaces.fast_api.deps.account import get_current_account
from application.account.use_cases.auth.auth import AuthUseCase, AuthRequestTelegramDTO, AuthRequestSignUpDTO, \
    AuthRequestLoginDTO

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/telegram/", response_model=AuthResponseDTO)
async def auth_via_telegram(dto: AuthRequestTelegramDTO) -> AuthResponseDTO:
    return await AuthUseCase().telegram(dto)


@router.get("/me/", response_model=AccountDTO)
async def get_me(account: AccountEntity = Depends(get_current_account)) -> AccountDTO:
    return await AuthUseCase().me(account)


@router.get("/profiles/", response_model=list[AccountAuthProfileDTO])
async def get_profiles(
        account: AccountEntity = Depends(get_current_account)
) -> list[AccountAuthProfileDTO]:
    return await AuthUseCase().profiles(account)


@router.post("/signup/", response_model=AuthResponseDTO)
async def signup(data: AuthRequestSignUpDTO) -> AuthResponseDTO:
    return await AuthUseCase().register(data)


@router.post("/login/", response_model=AuthResponseDTO)
async def login(data: AuthRequestLoginDTO) -> AuthResponseDTO:
    return await AuthUseCase().login(data)
