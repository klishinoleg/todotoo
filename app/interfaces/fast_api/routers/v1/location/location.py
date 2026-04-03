from application.location.use_cases.crud.location import LocationCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class LocationRouter(V1CrudRouter[LocationCrudUseCase]):
    prefix = "/locations"
    tags = ["v1/location"]
    use_case_cls = LocationCrudUseCase


location_crud_router = LocationRouter()
router = location_crud_router.router

