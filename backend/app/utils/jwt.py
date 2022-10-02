from datetime import timedelta
import jwt

from fastapi import HTTPException
from fastapi.security import HTTPBearer

from app.common.consts import JWT_ALGORITHM, JWT_SECRET, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES
from app.utils.date import get_now_datetime


class JWTAuth:
    algorithm = JWT_ALGORITHM
    secret = JWT_SECRET
    access_token_expires = int(JWT_ACCESS_TOKEN_EXPIRES)
    refresh_token_expires = int(JWT_REFRESH_TOKEN_EXPIRES)

    def encode_token(self, subject: str) -> str:
        now = get_now_datetime()
        payload = {
            "exp": now + timedelta(seconds=self.access_token_expires),
            "iat": now,
            "scope": "access_token",
            "sub": subject,
        }
        return jwt.encode(payload=payload, key=self.secret, algorithm=self.algorithm).decode("UTF-8")

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(jwt=token, key=self.secret, algorithms=[self.algorithm])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(status_code=401, detail="Scope for the token is invalid")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def encode_refresh_token(self, subject: str) -> str:
        now = get_now_datetime()
        payload = {
            "exp": now + timedelta(seconds=self.refresh_token_expires),
            "iat": now,
            "scope": "refresh_token",
            "sub": subject,
        }
        return jwt.encode(payload=payload, key=self.secret, algorithm=self.algorithm).decode("UTF-8")

    def refresh_token(self, token: str) -> str:
        try:
            payload = jwt.decode(jwt=token, key=self.secret, algorithms=[self.algorithm])
            if payload["scope"] == "refresh_token":
                subject = payload["sub"]
                access_token = self.encode_token(subject=subject)
                return access_token
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")


authorization = HTTPBearer()
auth_handler = JWTAuth()
