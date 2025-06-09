from pydantic import BaseModel
from litestar.plugins.pydantic import PydanticDTO


class Login(BaseModel):
    login: str
    password: str


LoginDTO = PydanticDTO[Login]
