from fastapi import APIRouter

from .event_comment import router as idea_event_comment_router
from .event_media import router as idea_event_media_router
from .event_participant import router as idea_event_participant_router
from .event_reaction import router as idea_event_reaction_router
from .idea_event import router as idea_event_router

router = APIRouter(tags=["v1/idea_event"])
router.include_router(idea_event_router)
router.include_router(idea_event_participant_router)
router.include_router(idea_event_media_router)
router.include_router(idea_event_comment_router)
router.include_router(idea_event_reaction_router)

