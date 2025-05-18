from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from advanced_alchemy.base import BigIntBase


class UserModel(BigIntBase):
    __tablename__ = "users"
    login: Mapped[str] = mapped_column(
        unique=True
    )
    first_name: Mapped[str]
    last_name: Mapped[str]
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        server_default=func.now()
    )
    password: Mapped[str]
