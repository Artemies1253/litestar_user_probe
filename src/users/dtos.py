from datetime import datetime

from pydantic import BaseModel, Field
from litestar.dto import DTOConfig
from litestar.plugins.pydantic import PydanticDTO


class User(BaseModel):
    id: int
    login: str
    first_name: str
    last_name: str
    created_date: datetime = Field(default_factory=datetime.now)
    password: str
    is_supper_user: bool


class CreateUser(BaseModel):
    login: str
    first_name: str
    last_name: str
    password: str


class UpdateUser(BaseModel):
    login: str
    first_name: str
    last_name: str


CreateUserDTO = PydanticDTO[CreateUser]
UpdateUserDTO = PydanticDTO[UpdateUser]


class UserWithoutPasswordDTO(PydanticDTO[User]):
    config = DTOConfig(exclude={"password"}, partial=True)
