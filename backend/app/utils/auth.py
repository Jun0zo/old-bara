from typing import Optional

from sqlalchemy.orm import Session
from app.database.schema import User, Permission


def get_permission_info(session: Session, user_id: int) -> Optional[Permission]:
    current_user = User.get(session=session, id=user_id, status="accepted")
    if current_user:
        return Permission.get(session=session, user_id=current_user.id)

    return
