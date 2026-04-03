from fastapi import APIRouter

from .idea import router as idea_router

router = APIRouter(tags=["v1/idea"])
router.include_router(idea_router)

