from os import environ

JWT_SECRET = environ.get("JWT_SECRET")
JWT_ALGORITHM = environ.get("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRES = environ.get("JWT_ACCESS_TOKEN_EXPIRES")
JWT_REFRESH_TOKEN_EXPIRES = environ.get("JWT_REFRESH_TOKEN_EXPIRES")
GMAIL_ADDR = environ.get("GMAIL_ADDR")
SUPERUSER_EMAIL = environ.get("SUPERUSER_EMAIL")
SUPERUSER_PW = environ.get("SUPERUSER_PW")
SUPERUSER_NAME = environ.get("SUPERUSER_NAME")
SUPERUSER_ROLE = environ.get("SUPERUSER_ROLE")
