from dataclasses import asdict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.common.config import conf
from app.database.conn import Base
from app.utils.create_superuser import create_superuser


def init_db() -> None:
    conf_dict = asdict(conf())
    database_url = conf_dict["DB_URL"]
    echo = conf_dict["DB_ECHO"]
    pool_recycle = conf_dict["DB_POOL_RECYCLE"]
    pool_size = conf_dict["DB_POOL_SIZE"]
    max_overflow = conf_dict["DB_MAX_OVERFLOW"]

    engine = create_engine(
        url=database_url,
        echo=echo,
        pool_recycle=pool_recycle,
        pool_pre_ping=True,
        pool_size=pool_size,
        max_overflow=max_overflow,
    )

    Base.metadata.create_all(engine)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = session()
    create_superuser(db_session)
    session.close_all()
    engine.dispose()


if __name__ == "__main__":
    init_db()
