from litestar import Litestar
from litestar_granian import GranianPlugin
from litestar.plugins.pydantic import PydanticPlugin
from advanced_alchemy.config import AlembicAsyncConfig
import pytest_asyncio
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from sqlalchemy.exc import OperationalError

from src.users.controllers import UserController
from src.base.settings import DEBUG
from src.base.settings import TEST_SQLALCHEMY_DATABASE_URL
from src.authorization.controllers import AuthorizationController
from src.authorization.jwt import jwt_auth
from users.repositories import UserModel
from users.tests.data import test_admin_data
from users.dtos import User

sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=TEST_SQLALCHEMY_DATABASE_URL,
    before_send_handler="autocommit",
    session_config=AsyncSessionConfig(expire_on_commit=False),
    create_all=True,
    alembic_config=AlembicAsyncConfig(
        script_location="./migrations/"
    )
)
test_advanced_alchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)

_test_app = Litestar(
    plugins=[GranianPlugin(), PydanticPlugin(), test_advanced_alchemy_plugin],
    route_handlers=[UserController, AuthorizationController],
    on_app_init=[jwt_auth.on_app_init],
    middleware=[jwt_auth.middleware],
    debug=DEBUG
)
_test_app.state.session_maker_class = sqlalchemy_config.create_session_maker()
_test_app.state.session_maker_class_1 = sqlalchemy_config.create_session_maker()



@pytest_asyncio.fixture(scope="session", autouse=True)
async def session():
    engine = sqlalchemy_config.get_engine()
    async with engine.begin() as conn:
        try:
            await conn.run_sync(sqlalchemy_config.metadata.create_all)
        except OperationalError as exc:
            print(f"Could not create test DB tables: {exc}")

    async with sqlalchemy_config.get_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(sqlalchemy_config.metadata.drop_all)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def admin_user(session: None) -> User:
    async with sqlalchemy_config.get_session() as session:  # или client.app.state.db
        user = UserModel(
            **test_admin_data
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return User(**user.__dict__)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def auth_header(session: None) -> dict:
    token = jwt_auth.create_token(identifier="1")
    return {"Authorization": f"Bearer {token}"}
