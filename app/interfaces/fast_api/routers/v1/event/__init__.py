from fastapi import APIRouter

from .event import router as event_router
from .event_member import router as event_member_router
from .event_occurrence import router as event_occurrence_router
from .event_occurrence_message import router as event_occurrence_message_router
from .event_schedule_rule import router as event_schedule_rule_router

router = APIRouter(tags=["v1/event"])
router.include_router(event_router)
router.include_router(event_member_router)
router.include_router(event_occurrence_router)
router.include_router(event_occurrence_message_router)
router.include_router(event_schedule_rule_router)

