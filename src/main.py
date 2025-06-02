from authorization.controllers import AuthorizationController
from authorization.jwt import jwt_auth
from litestar import Litestar
from litestar_granian import GranianPlugin
from litestar.plugins.pydantic import PydanticPlugin

from src.base.database import advanced_alchemy_plugin, ApplicationCore
from src.users.controllers import UserController
from src.base.settings import DEBUG


app = Litestar(
    plugins=[GranianPlugin(), PydanticPlugin(), advanced_alchemy_plugin, ApplicationCore()],
    route_handlers=[UserController, AuthorizationController],
    on_app_init=[jwt_auth.on_app_init],
    middleware=[jwt_auth.middleware],
    debug=DEBUG
)
