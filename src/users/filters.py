from __future__ import annotations

from pydantic import BaseModel


class UserListFilter(BaseModel):
    login_like: str | None = None
    first_name_equal: str | None = None
    ids: list | None = None

    limit: int = 20
    offset: int = 0
