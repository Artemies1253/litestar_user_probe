from authorization.services import retrieve_user_handler
from litestar.security.jwt import JWTAuth

from base.settings import SECRET_KEY
from users.dtos import User

jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=SECRET_KEY,
    exclude=["/login", "/schema"],
)
