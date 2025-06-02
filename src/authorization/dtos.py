from datetime import datetime

from pydantic import BaseModel, Field
from litestar.dto import DTOConfig
from litestar.plugins.pydantic import PydanticDTO


class Login(BaseModel):
    login: str
    password: str


LoginDTO = PydanticDTO[Login]
