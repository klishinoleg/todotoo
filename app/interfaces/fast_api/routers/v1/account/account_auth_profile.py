from application.account.use_cases.crud.account_auth_profile import AccountAuthProfileCrudUseCase
from interfaces.fast_api.routers.v1.base.crud import V1CrudRouter


class AccountAuthProfileRouter(V1CrudRouter[AccountAuthProfileCrudUseCase]):
    prefix = "/account-auth-profiles"
    tags = ["v1/account"]
    use_case_cls = AccountAuthProfileCrudUseCase


account_auth_profile_crud_router = AccountAuthProfileRouter()
router = account_auth_profile_crud_router.router

