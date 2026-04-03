from fastapi import APIRouter

from .meeting import router as meeting_router
from .meeting_participant import router as meeting_participant_router

router = APIRouter(tags=["v1/meeting"])
router.include_router(meeting_router)
router.include_router(meeting_participant_router)

