from fastapi import APIRouter

from .location import router as location_router

router = APIRouter(tags=["v1/location"])
router.include_router(location_router)

