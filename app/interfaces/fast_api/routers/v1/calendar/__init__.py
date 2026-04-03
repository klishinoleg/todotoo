from fastapi import APIRouter

from .calendar_item import router as calendar_item_router

router = APIRouter(tags=["v1/calendar"])
router.include_router(calendar_item_router)

