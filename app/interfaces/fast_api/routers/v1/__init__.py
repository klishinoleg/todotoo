from fastapi import APIRouter

from .account import router as account_router
from .activity_log import router as activity_log_router
from .calendar import router as calendar_router
from .config import router as config_router
from .discussion import router as discussion_router
from .event import router as event_router
from .idea import router as idea_router
from .idea_event import router as idea_event_router
from .idea_participant import router as idea_participant_router
from .location import router as location_router
from .meeting import router as meeting_router
from .motivation import router as motivation_router
from .plan import router as plan_router
from .tag import router as tag_router

router = APIRouter(tags=["v1"])
router.include_router(config_router)
router.include_router(account_router)
router.include_router(event_router)
router.include_router(location_router)
router.include_router(tag_router)
router.include_router(idea_router)
router.include_router(idea_participant_router)
router.include_router(plan_router)
router.include_router(meeting_router)
router.include_router(idea_event_router)
router.include_router(discussion_router)
router.include_router(motivation_router)
router.include_router(activity_log_router)
router.include_router(calendar_router)

