from fastapi import APIRouter

from application.config.dto.enums import EnumsConfigDTO
from application.config.use_cases.enums import ConfigEnumsUseCase

router = APIRouter(prefix="/config", tags=["v1/config"])


@router.get("/enums/", response_model=EnumsConfigDTO)
async def get_enums() -> EnumsConfigDTO:
    return await ConfigEnumsUseCase().get_enums()

