from typing import Any

from authorization.dtos import Login, LoginDTO
from authorization.jwt import jwt_auth
from authorization.services import authenticate_user
from litestar import Controller, post, Response
from sqlalchemy.ext.asyncio import AsyncSession
from users.repositories import UserRepositoryService


class AuthorizationController(Controller):
    tags = ["authorization"]
    path = "/authorization"

    @post("/login", dto=LoginDTO)
    async def get_token(self, data: Login, db_session: AsyncSession) -> Response[dict[str, Any]]:
        """I create user_repository manually to write how it works"""
        user_repository = UserRepositoryService(session=db_session)
        user = await authenticate_user(login=data.login, password=data.password, user_service=user_repository)
        token = jwt_auth.create_token(identifier=str(user.id))

        return Response(
            content={
                "user_id": int(user.id),
                "access_token": token,
            },
            media_type="application/json"
        )
