from fastapi import APIRouter

from .tag import router as tag_router

router = APIRouter(tags=["v1/tag"])
router.include_router(tag_router)

