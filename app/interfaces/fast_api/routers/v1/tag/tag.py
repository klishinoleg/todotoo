from application.tag.use_cases.crud.tag import TagCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class TagRouter(V1CrudRouter[TagCrudUseCase]):
    prefix = "/tags"
    tags = ["v1/tag"]
    use_case_cls = TagCrudUseCase


tag_crud_router = TagRouter()
router = tag_crud_router.router

