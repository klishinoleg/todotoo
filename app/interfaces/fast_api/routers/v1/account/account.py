from application.account.use_cases.crud.account import AccountCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class AccountRouter(V1CrudRouter[AccountCrudUseCase]):
    prefix = "/accounts"
    tags = ["v1/account"]
    use_case_cls = AccountCrudUseCase


account_crud_router = AccountRouter()
router = account_crud_router.router

