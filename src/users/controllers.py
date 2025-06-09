from base.settings import BASE_PAGE_LIMIT
from base.validators import is_ids_valid
from litestar import Controller, get, post, put, delete, Request
from advanced_alchemy.extensions.litestar import providers
from advanced_alchemy import service
from litestar.exceptions import HTTPException
from litestar.params import Parameter
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from pydantic import ValidationError

from src.users.dtos import UserWithoutPasswordDTO, User, CreateUser, CreateUserDTO, UpdateUser, UpdateUserDTO
from typing_extensions import Annotated
from users.filters import UserListFilter
from users.repositories import UserRepositoryService
from users.services import create_user, get_user, get_user_list, update_user, delete_user


class UserController(Controller):
    tags = ["User"]
    path = "/users"
    return_dto = UserWithoutPasswordDTO

    dependencies = providers.create_service_dependencies(UserRepositoryService, "user_service", )

    @get("/")
    async def get_user_list(
            self,
            user_service: UserRepositoryService,
            login_like: str | None = None, first_name_equal: str | None = None,
            limit: int = BASE_PAGE_LIMIT, offset: int = 0,
            ids: Annotated[str, Parameter(description="список id", pattern=r'^[0-9, ]*$')] | None = None,
    ) -> service.OffsetPagination[User]:
        try:
            if ids and is_ids_valid(ids):
                ids = list(map(int, map(str.strip, ids.split(","))))
            else:
                ids = []
            user_filter = UserListFilter(
                login_like=login_like, first_name_equal=first_name_equal, ids=ids, limit=limit, offset=offset
            )

            return await get_user_list(user_filters=user_filter, user_service=user_service)
        except ValidationError:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="bad request")

    @post("/", dto=CreateUserDTO)
    async def create_user(self, request: Request, user_service: UserRepositoryService, data: CreateUser) -> User:
        if request.user.is_supper_user:
            return await create_user(user_service=user_service, user_create_data=data)
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="forbidden")

    @get("/{id:int}")
    async def get_user(self, id: int, user_service: UserRepositoryService) -> User:
        return await get_user(user_id=id, user_service=user_service)

    @put("/{id:int}", dto=UpdateUserDTO)
    async def update_user(
            self, request: Request, id: int, user_service: UserRepositoryService, data: UpdateUser
    ) -> User:
        if request.user.is_supper_user or request.user.id == id:
            return await update_user(user_id=id, user_service=user_service, user_data=data)
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="forbidden")

    @delete("/{id:int}")
    async def delete_user(self, request: Request, id: int, user_service: UserRepositoryService) -> None:
        if request.user.is_supper_user or request.user.id == id:
            await delete_user(user_id=id, user_service=user_service)
        else:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="forbidden")
