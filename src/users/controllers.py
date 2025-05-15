from advanced_alchemy.extensions.litestar.providers import FilterConfig
from litestar import Controller, get, post
from advanced_alchemy.extensions.litestar import providers

from src.users.dtos import UserWithoutPasswordDTO, User
from users.repositories import UserRepositoryService


class UserController(Controller):
    path = "/users"
    return_dto = UserWithoutPasswordDTO

    dependencies = providers.create_service_dependencies(
        UserRepositoryService,
        "user_service",
        filters=FilterConfig(pagination_type="limit_offset", search="first_name")
    )

    @get("/")
    async def get_user_list(self) -> list[User]:
        admin = User(id=1, first_name="Dean", last_name="Vinchester", password="1234")
        return [admin]

