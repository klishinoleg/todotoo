from application.account.use_cases.crud.account_session import AccountSessionCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class AccountSessionRouter(V1CrudRouter[AccountSessionCrudUseCase]):
    prefix = "/account-sessions"
    tags = ["v1/account"]
    use_case_cls = AccountSessionCrudUseCase


account_session_crud_router = AccountSessionRouter()
router = account_session_crud_router.router

