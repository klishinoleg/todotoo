from application.idea_participant.use_cases.crud.participation_request import ParticipationRequestCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class ParticipationRequestRouter(V1CrudRouter[ParticipationRequestCrudUseCase]):
    prefix = "/participation-requests"
    tags = ["v1/idea_participant"]
    use_case_cls = ParticipationRequestCrudUseCase


participation_request_crud_router = ParticipationRequestRouter()
router = participation_request_crud_router.router

