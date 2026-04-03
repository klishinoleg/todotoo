from fastapi import APIRouter

from .enums import router as enums_router

router = APIRouter(tags=["v1/config"])
router.include_router(enums_router)

