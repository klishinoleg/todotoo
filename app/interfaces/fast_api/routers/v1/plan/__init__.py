from fastapi import APIRouter

from .plan import router as plan_router
from .plan_step import router as plan_step_router

router = APIRouter(tags=["v1/plan"])
router.include_router(plan_router)
router.include_router(plan_step_router)

