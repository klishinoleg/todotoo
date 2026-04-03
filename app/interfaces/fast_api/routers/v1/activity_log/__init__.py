from fastapi import APIRouter

from .idea_activity import router as idea_activity_router

router = APIRouter(tags=["v1/activity_log"])
router.include_router(idea_activity_router)

