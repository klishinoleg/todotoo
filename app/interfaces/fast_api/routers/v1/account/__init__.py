from fastapi import APIRouter

from .account import router as account_router
from .account_auth_profile import router as account_auth_profile_router
from .account_session import router as account_session_router

router = APIRouter(tags=["v1/account"])
router.include_router(account_router)
router.include_router(account_auth_profile_router)
router.include_router(account_session_router)

