from fastapi import APIRouter

from .motivator import router as motivator_router

router = APIRouter(tags=["v1/motivation"])
router.include_router(motivator_router)

