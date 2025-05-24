from advanced_alchemy import service
from advanced_alchemy.filters import CollectionFilter, ComparisonFilter, SearchFilter, LimitOffset
from passlib.context import CryptContext
from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from users.dtos import CreateUser, User, UpdateUser
from users.filters import UserListFilter
from users.repositories import UserRepositoryService


def verify_password(plain_password, hashed_password):
    """Проверка соответствия пароля и хеша"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Дать захешированную версию пароля"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


async def create_user(user_service: UserRepositoryService, user_create_data: CreateUser) -> User:
    user_create_data.password = get_password_hash(user_create_data.password)
    try:
        user = await user_service.create(user_create_data)
    except DuplicateKeyError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="login is already exist")

    return user_service.to_schema(user, schema_type=User)


async def get_user(user_id: int, user_service: UserRepositoryService) -> User:
    try:
        user = await user_service.get(item_id=user_id)
    except NotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Not found")

    return user_service.to_schema(user, schema_type=User)


async def update_user(user_id: int, user_service: UserRepositoryService, user_data: UpdateUser) -> User:
    try:
        user = await user_service.update(user_data, item_id=user_id, auto_commit=True)
    except NotFoundError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Not found")
    except DuplicateKeyError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="login is already exist")

    return user_service.to_schema(user, schema_type=User)


def get_alchemy_user_filters(user_filters: UserListFilter) -> list[LimitOffset, list[SearchFilter]]:
    filters = []
    pagination = LimitOffset(limit=user_filters.limit, offset=user_filters.offset)
    filters.append(pagination)

    if user_filters.login_like:
        login_like_filter = SearchFilter(field_name="login", value=user_filters.login_like)
        filters.append(login_like_filter)

    if user_filters.first_name_equal:
        first_name_equal = ComparisonFilter(field_name="first_name", operator="eq", value=user_filters.first_name_equal)
        filters.append(first_name_equal)

    if user_filters.ids:
        ids_filter = CollectionFilter(field_name="id", values=user_filters.ids)
        filters.append(ids_filter)

    return filters


async def get_user_list(
        user_filters: UserListFilter, user_service: UserRepositoryService
) -> service.OffsetPagination[User]:
    filters = get_alchemy_user_filters(user_filters=user_filters)
    results, total = await user_service.list_and_count(*filters)
    return user_service.to_schema(results, total, filters=filters, schema_type=User)
