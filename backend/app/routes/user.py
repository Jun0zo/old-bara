from dataclasses import asdict
from operator import itemgetter
import re
from uuid import uuid4

import bcrypt
from fastapi import APIRouter, Depends, Security
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.common.config import conf
from app.database.conn import db
from app.database.schema import Permission, User, UserRole
from app.models import (
    UserRoleCreate,
    UserRoleUpdate,
    UserRegister,
    UserUpdate,
    UserLogin,
    ResetPassword,
)
from app.responses import (
    create_role_response,
    get_all_role_response,
    get_specific_role_response,
    update_role_response,
    delete_role_response,
    create_user_response,
    get_all_user_response,
    get_specific_user_response,
    update_user_response,
    delete_user_response,
    login_response,
    refresh_response,
    verify_email_response,
    send_password_reset_mail_response,
    reset_password_response,
)
from app.utils.auth import get_permission_info
from app.utils.jwt import auth_handler, authorization
from app.utils.gmail import send


router = APIRouter(prefix="/user")
config = asdict(conf())


@router.post("/role", status_code=201, responses=create_role_response())
async def create_role(
    request_info: UserRoleCreate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `Role 생성 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_role_name_valid = validate_role_name(request_info.name)
    if not is_role_name_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_role_name_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)

    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if UserRole.get(session=session, name=request_info.name):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 존재하는 역할입니다!"))
    try:
        created_object_id = UserRole.create(session=session, auto_commit=True, name=request_info.name).id
        return JSONResponse(status_code=201,
                            content=dict(success=True, message="OK",
                                         result=dict(created_object_id=created_object_id)))
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.get("/role", status_code=200, responses=get_all_role_response())
async def get_all_role(
    session: Session = Depends(db.session), jwt_token: HTTPAuthorizationCredentials = Security(authorization)
) -> JSONResponse:
    """
    `모든 Role 정보 받아오는 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    roles = UserRole.filter(session=session, with_entities=[UserRole.id, UserRole.name]).order_by("id").all()
    result = {"success": True, "message": "OK", "result": roles}
    return result


@router.get("/role/{target_role_id}", status_code=200, responses=get_specific_role_response())
async def get_specific_role(
    target_role_id: int,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `특정 Role 정보 받아오는 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    role = UserRole.get(session=session, id=target_role_id, with_entities=[UserRole.id, UserRole.name])
    if not role:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 역할입니다!"))

    result = {"success": True, "message": "OK", "result": role}
    return result


@router.put("/role/{target_role_id}", status_code=200, responses=update_role_response())
async def update_role(
    target_role_id: int,
    request_info: UserRoleUpdate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `Role update API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_role_name_valid = validate_role_name(request_info.name)
    if not is_role_name_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_role_name_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if not UserRole.get(session=session, id=target_role_id):
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 역할입니다!"))

    if UserRole.get(session=session, name=request_info.name):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 존재하는 역할 이름입니다!"))

    try:
        UserRole.filter(session=session, id=target_role_id).update(auto_commit=True, name=request_info.name)
        return JSONResponse(status_code=200,
                            content=dict(success=True, message="OK",
                                         result=dict(updated_object_id=target_role_id)))
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.delete("/role/{target_role_id}", status_code=200, responses=delete_role_response())
async def delete_role(
    target_role_id: int,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `Role 삭제 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if not UserRole.get(session=session, id=target_role_id):
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 역할입니다!"))

    if User.get(session=session, role_id=target_role_id):
        return JSONResponse(status_code=400, content=dict(success=False, message="해당 역할로 지정된 사용자가 1명 이상 존재합니다!\n" +
                                                                                 "사용자의 역할을 다른 역할로 변경한 후에 다시 시도해 주세요!"))
    try:
        UserRole.filter(session=session, id=target_role_id).delete(auto_commit=True)
        return JSONResponse(status_code=200, content=dict(success=True, message="OK",
                                                          result=dict(deleted_object_id=target_role_id)))
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.post("", status_code=201, responses=create_user_response())
async def create_user(request_info: UserRegister, session: Session = Depends(db.session)) -> JSONResponse:
    """
    `User 생성 API`
    """
    is_password_valid = validate_password(request_info.password)
    if not is_password_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_password_valid["detail"]))

    is_name_valid = validate_name(request_info.name)
    if not is_name_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_name_valid["detail"]))

    user = User.get(session=session, email=request_info.email)
    if user:
        if user.status != "registered":
            return JSONResponse(status_code=400, content=dict(success=False, message="이미 존재하는 이메일입니다!"))
        try:
            User.filter(session=session, id=user.id).delete(auto_commit=True)
        except Exception as e:
            print(e)
            return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))

    email_token = uuid4().hex
    hashed_password = bcrypt.hashpw(request_info.password.encode("utf-8"), bcrypt.gensalt())
    try:
        created_object_id = User.create(
            session=session,
            auto_commit=True,
            email=request_info.email,
            email_token=email_token,
            password=hashed_password,
            name=request_info.name,
        ).id
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))

    try:
        mail_content = f"<p><a href='{config['SERVER_URL']}/api/user/verify-email/{email_token}' target='_blank'>" + \
            "여기를 클릭해 회원가입을 완료해 주세요!</a></p>"
        send(destination=request_info.email,
             subject=f"{config['SERVICE_NAME']} 회원가입 인증 메일입니다.",
             body=f"{mail_content}")
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="회원가입 인증 메일 전송 중 오류가 발생했습니다!"))

    return JSONResponse(status_code=201, content=dict(success=True, message="OK",
                                                      result=dict(created_object_id=created_object_id)))


@router.get("", status_code=200, responses=get_all_user_response())
async def get_all_user(
    session: Session = Depends(db.session), jwt_token: HTTPAuthorizationCredentials = Security(authorization)
) -> JSONResponse:
    """
    `모든 User 정보 받아오는 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
    if "AR" not in permission_info.user:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    users_verified = User.filter(
        session=session, status="verified", with_entities=[User.id, User.email, User.name, User.status]
    ).all()

    users_accpted_or_deleted = (
        session.query(User)
        .filter(User.status.in_(["accepted", "deleted"]))
        .join(UserRole, User.role_id == UserRole.id)
        .join(Permission, User.id == Permission.user_id)
        .with_entities(
            User.id,
            User.email,
            User.name,
            User.role_id,
            UserRole.name.label("role_name"),
            User.status,
            User.plate_fee,
            User.contract_fee,
            Permission.user.label("permission_user"),
            Permission.transaction.label("permission_transaction"),
            Permission.invoice.label("permission_invoice"),
        )
        .all()
    )
    users = sorted(users_verified + users_accpted_or_deleted, key=itemgetter("id"), reverse=False)
    result = {"success": True, "message": "OK", "result": users}
    return result


@router.get("/{target_user_id}", status_code=200, responses=get_specific_user_response())
async def get_specific_user(
    target_user_id: int = None,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `특정 User 정보 받아오는 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))
    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if target_user_id != user_id_from_jwt and "AR" not in permission_info.user:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    user_verified = User.filter(
        session=session,
        id=target_user_id,
        status="verified",
        with_entities=[User.id, User.email, User.name, User.status],
    ).first()

    if user_verified:
        user = user_verified
    else:
        user_accpted_or_deleted = (
            session.query(User)
            .filter(User.id == target_user_id, User.status.in_(["accepted", "deleted"]))
            .join(UserRole, User.role_id == UserRole.id)
            .join(Permission, User.id == Permission.user_id)
            .with_entities(
                User.id,
                User.email,
                User.name,
                User.role_id,
                UserRole.name.label("role_name"),
                User.status,
                User.plate_fee,
                User.contract_fee,
                Permission.user.label("permission_user"),
                Permission.transaction.label("permission_transaction"),
                Permission.invoice.label("permission_invoice"),
            )
            .first()
        )
        user = user_accpted_or_deleted

    if not user:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다!"))

    result = {"success": True, "message": "OK", "result": user}
    return result


@router.put("/{target_user_id}", status_code=200, responses=update_user_response())
async def update_user(
    target_user_id: int,
    request_info: UserUpdate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `User update API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    target_user = User.filter(session=session, id=target_user_id,
                              status__in=["verified", "accepted", "deleted"]).first()
    if not target_user:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다!"))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if user_id_from_jwt == target_user_id:
        if not (request_info.current_password and request_info.new_password and request_info.new_password_check):
            return JSONResponse(status_code=400, content=dict(success=False, message="모든 값을 입력해 주세요!"))
        if request_info.new_password != request_info.new_password_check:
            return JSONResponse(status_code=400, content=dict(success=False, message="비밀번호와 비밀번호 확인값이 일치하지 않습니다!"))
        if not bcrypt.checkpw(request_info.current_password.encode("utf-8"), target_user.password.encode("utf-8")):
            return JSONResponse(status_code=400, content=dict(success=False, message="비밀번호가 틀립니다!"))
        hashed_password = bcrypt.hashpw(request_info.new_password.encode("utf-8"), bcrypt.gensalt())
        try:
            User.filter(session=session, id=target_user_id).update(auto_commit=True, password=hashed_password)
        except Exception as e:
            print(e)
            return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))
        result = {"updated_object_id": target_user_id}
        return JSONResponse(status_code=200, content=dict(success=True, message="OK", result=result))

    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    to_update_at_user = {}
    to_update_at_permission = {}
    if request_info.name is not None:
        is_name_valid = validate_name(request_info.name)
        if not is_name_valid["success"]:
            return JSONResponse(status_code=400, content=dict(success=False, message=is_name_valid["detail"]))
        to_update_at_user["name"] = request_info.name

    if request_info.role_id is None:
        if not target_user.role_id:
            return JSONResponse(status_code=400, content=dict(success=False, message="역할은 반드시 지정해야 합니다!"))
    else:
        if not UserRole.get(session=session, id=request_info.role_id):
            return JSONResponse(status_code=400, content=dict(success=False, message="변경 대상 역할이 존재하지 않습니다!"))
        to_update_at_user["role_id"] = request_info.role_id

    if target_user.status == "verified":
        to_update_at_user["status"] = "accepted"

    if request_info.plate_fee is not None:
        to_update_at_user["plate_fee"] = request_info.plate_fee

    if request_info.contract_fee is not None:
        to_update_at_user["contract_fee"] = request_info.contract_fee

    if not Permission.get(session=session, user_id=target_user.id):
        if not (
            request_info.permission_user
            and request_info.permission_transaction
            and request_info.permission_invoice
        ):
            return JSONResponse(
                status_code=400, content=dict(success=False, message="현재 사용자의 권한이 지정되어 있지 않습니다. 권한을 지정해 주세요!"))

    if request_info.permission_user is not None:
        to_update_at_permission["user"] = request_info.permission_user

    if request_info.permission_transaction is not None:
        to_update_at_permission["transaction"] = request_info.permission_transaction

    if request_info.permission_invoice is not None:
        to_update_at_permission["invoice"] = request_info.permission_invoice

    if not to_update_at_user and to_update_at_permission:
        return JSONResponse(status_code=400, content=dict(success=False, message="수정할 값을 입력해 주세요!"))

    if to_update_at_user:
        try:
            User.filter(session=session, id=target_user_id).update(auto_commit=True, **to_update_at_user)
        except Exception as e:
            print(e)
            return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))

    if to_update_at_permission:
        if not Permission.get(session=session, user_id=target_user_id):
            try:
                Permission.create(session=session, auto_commit=True, user_id=target_user_id, **to_update_at_permission)
            except Exception as e:
                print(e)
                return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))
        try:
            Permission.filter(session=session, user_id=target_user_id).update(
                auto_commit=True, user_id=target_user_id, **to_update_at_permission
            )
        except Exception as e:
            print(e)
            return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))

    return JSONResponse(status_code=200, content=dict(success=True, message="OK",
                                                      result=dict(updated_object_id=target_user_id)))


@router.delete("/{target_user_id}", status_code=200, responses=delete_user_response())
async def delete_user(
    target_user_id: int,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `User update API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))
    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if user_id_from_jwt == target_user_id:
        return JSONResponse(status_code=400, content=dict(success=False, message="본인 계정은 삭제할 수 없습니다!"))

    target_user = User.get(session=session, id=target_user_id)
    if not target_user:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다!"))

    if target_user.status == "deleted":
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 탈퇴된 계정입니다!"))

    elif target_user.status in ["registered", "verified"]:
        try:
            User.filter(session=session, id=target_user_id).delete(auto_commit=True)
        except Exception as e:
            print(e)
            return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))

        return JSONResponse(status_code=200, content=dict(success=True, message="OK",
                                                          result=dict(deleted_object_id=target_user_id)))

    try:
        User.filter(session=session, id=target_user_id).update(auto_commit=True, status="deleted")
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))

    return JSONResponse(status_code=200, content=dict(success=True, message="OK",
                                                      result=dict(withdrawn_object_id=target_user_id)))


@router.post("/login", status_code=200, responses=login_response())
async def login(request_info: UserLogin, session: Session = Depends(db.session)) -> JSONResponse:
    """
    `로그인 API`
    """
    user = User.get(session=session, email=request_info.email)
    if not user:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다!"))

    if user.status == "registered":
        return JSONResponse(
            status_code=400, content=dict(success=False, message="이메일 인증을 완료해 주세요!\n인증 메일이 도착하지 않았다면 스팸 메일함을 확인해 주세요!")
        )
    elif user.status == "verified":
        return JSONResponse(status_code=400, content=dict(success=False, message="관리자 승인 대기 중인 계정입니다!"))
    elif user.status == "deleted":
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다!"))

    if not bcrypt.checkpw(request_info.password.encode("utf-8"), user.password.encode("utf-8")):
        return JSONResponse(status_code=400, content=dict(success=False, message="비밀번호가 틀립니다!"))

    access_token = auth_handler.encode_token(subject=str(user.id))
    refresh_token = auth_handler.encode_refresh_token(subject=str(user.id))

    return JSONResponse(
        status_code=200,
        content=dict(success=True, message="OK", access_token=access_token, refresh_token=refresh_token),
    )


@router.get("/token/refresh", status_code=200, responses=refresh_response())
async def refresh(jwt_token: HTTPAuthorizationCredentials = Security(authorization)) -> JSONResponse:
    """
    `Token refresh API`
    """
    token = jwt_token.credentials
    access_token = auth_handler.refresh_token(token)

    return JSONResponse(
        status_code=200,
        content=dict(success=True, message="OK", access_token=access_token),
    )


@router.get("/verify-email/{token}", status_code=307, responses=verify_email_response())
async def verify_email(token: str, session: Session = Depends(db.session)) -> JSONResponse:
    """
    `이메일 인증 API`
    """
    if not User.get(session=session, email_token=token, status="registered"):
        return HTMLResponse(
            status_code=400,
            content="<html><script>alert('인증 토큰이 유효하지 않습니다!');location.href='/';</script></html>"
        )

    try:
        User.filter(session=session, email_token=token).update(auto_commit=True, status="verified")
    except Exception as e:
        print(e)
        return HTMLResponse(
            status_code=409,
            content="<html><script>alert('예상치 못한 오류가 발생했습니다!');location.href='/';</script></html>"
        )

    return RedirectResponse(url=config["SERVER_URL"], status_code=307)


@router.get("/reset-password/{target_user_mail}", status_code=200, responses=send_password_reset_mail_response())
async def send_password_reset_mail(target_user_mail: EmailStr, session: Session = Depends(db.session)) -> JSONResponse:
    """
    `패스워드 초기화 메일 전송 API`
    """
    if not User.filter(session=session, email=target_user_mail, status__in=["verified", "accepted"]).first():
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다!"))

    email_token = uuid4().hex
    try:
        User.filter(session=session, email=target_user_mail).update(auto_commit=True, email_token=email_token)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))

    mail_content = f"<p><a href='{config['SERVER_URL']}/reset-password?token={email_token}' target='_blank'>" + \
        "여기를 클릭해 비밀번호 초기화를 진행해 주세요!</a></p>"
    send(destination=target_user_mail,
         subject=f"{config['SERVICE_NAME']} 비밀번호 초기화 메일입니다.",
         body=f"{mail_content}")

    return JSONResponse(status_code=200, content=dict(success=True, message="OK"))


@router.post("/reset-password", status_code=200, responses=reset_password_response())
async def reset_password(request_info: ResetPassword, session: Session = Depends(db.session)) -> JSONResponse:
    """
    `패스워드 초기화 API`
    """
    if not User.filter(session=session, email_token=request_info.token, status__in=["verified", "accepted"]).first():
        return JSONResponse(status_code=400, content=dict(success=False, message="인증 토큰이 유효하지 않습니다!"))

    if request_info.new_password != request_info.new_password_check:
        return JSONResponse(status_code=400, content=dict(success=False, message="비밀번호와 비밀번호 확인값이 일치하지 않습니다!"))

    hashed_password = bcrypt.hashpw(request_info.new_password.encode("utf-8"), bcrypt.gensalt())
    try:
        User.filter(session=session, email_token=request_info.token).update(auto_commit=True, password=hashed_password)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))

    updated_object_id = User.get(session=session, email_token=request_info.token).id
    result = {"updated_object_id": updated_object_id}
    return JSONResponse(status_code=200, content=dict(success=True, message="OK", result=result))


def validate_password(password: str) -> dict:
    result = {"detail": "", "success": False}
    if not (8 <= len(password) <= 20):
        result["detail"] = "비밀번호는 8자 이상, 20자 이하여야 합니다!"
        return result

    elif re.search("[0-9]+", password) is None:
        result["detail"] = "비밀번호는 최소 1개 이상의 숫자가 포함되어 있어야 합니다!"
        return result

    elif re.search("[a-zA-Z]+", password) is None:
        result["detail"] = "비밀번호는 최소 1개 이상의 영문 대문자 또는 소문자가 포함되어 있어야 합니다!"
        return result

    elif re.search("[`~!@#$%^&*.?]+", password) is None:
        result["detail"] = "비밀번호는 최소 1개 이상의 특수문자(~!@#$%^&*.?)가 포함되어 있어야 합니다!"
        return result

    else:
        result["detail"] = "OK"
        result["success"] = True
        return result


def validate_name(name: str) -> dict:
    result = {"detail": "", "success": False}
    if not (2 <= len(name) <= 10):
        result["detail"] = "이름은 2자 이상, 10자 이하여야 합니다!"
        return result

    elif " " in name:
        result["detail"] = "이름에는 공백이 포함될 수 없습니다!"
        return result

    elif re.search("[`~!@#$%^&*.?]+", name):
        result["detail"] = "이름에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"
        return result

    else:
        result["detail"] = "OK"
        result["success"] = True
        return result


def validate_role_name(name: str) -> dict:
    result = {"detail": "", "success": False}
    if not (2 <= len(name) <= 10):
        result["detail"] = "역할 이름은 2자 이상, 10자 이하여야 합니다!"
        return result

    elif " " in name:
        result["detail"] = "역할 이름에는 공백이 포함될 수 없습니다!"
        return result

    elif re.search("[`~!@#$%^&*.?]+", name):
        result["detail"] = "역할 이름에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"
        return result

    else:
        result["detail"] = "OK"
        result["success"] = True
        return result
