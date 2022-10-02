from dataclasses import dataclass, field
from os import path, environ
from typing import Optional
from urllib.parse import quote

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    """
    기본 Configuration
    """

    ALLOW_SITE: list = field(default_factory=lambda: ["*"])
    BASE_DIR: str = base_dir
    SERVICE_NAME: str = environ.get("SERVICE_NAME")
    SERVER_URL: str = environ.get("SERVER_URL")
    SWAGGER_URL: Optional[str] = "/docs"
    REDOC_URL: Optional[str] = "/redoc"
    DB_URL: str = (
        f"mysql+pymysql://root:{quote(environ.get('MYSQL_ROOT_PASSWORD'))}@{environ.get('MYSQL_HOST')}:"
        + f"{environ.get('MYSQL_PORT')}/{environ.get('MYSQL_DATABASE')}?charset=utf8mb4"
    )
    DB_ECHO: bool = False
    DB_POOL_RECYCLE: int = 900
    DB_POOL_SIZE: int = 30
    DB_MAX_OVERFLOW: int = 10
    TEST_MODE: bool = False
    DEBUG: bool = False


@dataclass
class LocalConfig(Config):
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    SWAGGER_URL: str = None
    REDOC_URL: str = None


@dataclass
class TestConfig(Config):
    TEST_MODE: bool = True
    DEBUG: bool = True


def conf():
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("RUNNING_ENV")]()
