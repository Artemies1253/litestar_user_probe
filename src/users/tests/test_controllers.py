import pytest
from authorization.jwt import jwt_auth

from litestar.testing import AsyncTestClient

from users.tests.conftest import _test_app
from users.dtos import User


@pytest.mark.asyncio
async def test_user_list_ok(auth_header: dict) -> None:
    client = AsyncTestClient(app=_test_app)
    response = await client.get("/users", headers=auth_header)
    assert response.status_code == 200

