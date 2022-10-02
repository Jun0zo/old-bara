import bcrypt
from sqlalchemy.orm import Session

from app.common.consts import SUPERUSER_EMAIL, SUPERUSER_PW, SUPERUSER_NAME, SUPERUSER_ROLE
from app.database.schema import UserRole, User, Permission


def create_superuser(session: Session) -> None:
    email = SUPERUSER_EMAIL
    password = SUPERUSER_PW
    name = SUPERUSER_NAME
    role = SUPERUSER_ROLE
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    if UserRole.get(session=session, name=role):
        return

    if User.get(session=session, email=email):
        return

    UserRole.create(session=session, auto_commit=True, name=role)
    User.create(
        session=session,
        auto_commit=True,
        email=email,
        email_token="",
        password=hashed_password,
        name=name,
        role_id=UserRole.get(session=session, name=role).id,
        status="accepted",
        plate_fee=0,
        contract_fee=0.0,
    )
    Permission.create(
        session=session,
        auto_commit=True,
        user_id=User.get(session=session, email=email).id,
        user="ARW",
        transaction="ARW",
        invoice="ARW",
    )
