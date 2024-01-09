from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users import FastAPIUsers
from auth.models import User
from auth.utils import get_user_manager
from config import SECRET_KEY

cookie_transport = CookieTransport(cookie_name="SelfPublisher", cookie_max_age=3600)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

user = fastapi_users.current_user()
verified_user = fastapi_users.current_user(verified=True)