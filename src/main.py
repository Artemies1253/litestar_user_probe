from litestar import Litestar
from litestar_granian import GranianPlugin
from litestar.plugins.pydantic import PydanticPlugin
from src.base.database import advanced_alchemy_plugin, ApplicationCore

from src.users.controllers import UserController


app = Litestar(
    plugins=[GranianPlugin(), PydanticPlugin(), advanced_alchemy_plugin, ApplicationCore()],
    route_handlers=[UserController]
)
