from advanced_alchemy.filters import SearchFilter, CollectionFilter, StatementFilter
from typing_extensions import Annotated

from advanced_alchemy.extensions.litestar.providers import FilterConfig
from litestar import Controller, get, post
from litestar.params import Dependency
from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy import filters, service

from src.users.dtos import UserWithoutPasswordDTO, User, CreateUser
from users.repositories import UserRepositoryService
from users.services import create_user, get_user


class UserController(Controller):
    path = "/users"
    return_dto = UserWithoutPasswordDTO

    dependencies = providers.create_service_dependencies(
        UserRepositoryService,
        "user_service",
        filters=FilterConfig(pagination_type="limit_offset", search="first_name,login")
    )

    @get("/")
    async def get_user_list(
            self,
            user_service: UserRepositoryService,
            filters: Annotated[list[StatementFilter], Dependency(skip_validation=True)],
            login: str | None = None, first_name: str | None = None,
    ) -> service.OffsetPagination[User]:
        results, total = await user_service.list_and_count(*filters)
        return user_service.to_schema(results, total, filters=filters, schema_type=User)

    @post("/")
    async def create_user(self, user_service: UserRepositoryService, data: CreateUser) -> User:
        return await create_user(user_service=user_service, user_create_data=data)

    @get("/{id:int}")
    async def get_user(self, id: int, user_service: UserRepositoryService) -> User:
        return await get_user(user_id=id, user_service=user_service)
