import jwt

from app.common.consts import JWT_ALGORITHM, JWT_SECRET
from app.utils.date import get_now_datetime


def create_expired_jwt() -> str:
    algorithm = JWT_ALGORITHM
    secret = JWT_SECRET
    now = get_now_datetime()
    payload = {
        "exp": 0,
        "iat": now,
        "scope": "access_token",
        "sub": "1",
    }
    return jwt.encode(payload=payload, key=secret, algorithm=algorithm).decode("UTF-8")
