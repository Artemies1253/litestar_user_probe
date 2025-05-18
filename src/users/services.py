from passlib.context import CryptContext
from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST

from users.dtos import CreateUser, User
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
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Not found")

    return user_service.to_schema(user, schema_type=User)