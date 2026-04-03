from application.activity_log.use_cases.crud.idea_activity import IdeaActivityCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class IdeaActivityRouter(V1CrudRouter[IdeaActivityCrudUseCase]):
    prefix = "/idea-activities"
    tags = ["v1/activity_log"]
    use_case_cls = IdeaActivityCrudUseCase


idea_activity_crud_router = IdeaActivityRouter()
router = idea_activity_crud_router.router

