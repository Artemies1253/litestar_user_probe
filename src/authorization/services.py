from advanced_alchemy.filters import ComparisonFilter
from litestar.connection import ASGIConnection
from litestar.security.jwt import Token
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST
from sqlalchemy.ext.asyncio import AsyncSession

from users.dtos import User
from users.repositories import UserRepositoryService
from users.services import get_user, verify_password


async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User:
    session_factory = connection.app.state.session_maker_class

    async with session_factory() as session:  # type: AsyncSession
        user_repository = UserRepositoryService(session=session)
        return await get_user(user_id=int(token.sub), user_service=user_repository)



async def authenticate_user(login: str, password: str, user_service: UserRepositoryService):
    """Вернуть авторизованного пользователя"""
    login_equal = ComparisonFilter(field_name="login", operator="eq", value=login)
    filters = [login_equal]
    user = await user_service.get_one_or_none(*filters)

    if not user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="bad request")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="bad request")
    return user
