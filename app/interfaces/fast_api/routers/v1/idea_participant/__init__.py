from fastapi import APIRouter

from .idea_participant import router as idea_participant_router
from .participation_request import router as participation_request_router

router = APIRouter(tags=["v1/idea_participant"])
router.include_router(idea_participant_router)
router.include_router(participation_request_router)

