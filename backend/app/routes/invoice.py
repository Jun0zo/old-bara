from calendar import monthrange
from datetime import datetime
from typing import Union

from fastapi import APIRouter, Depends, Security
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.database.conn import db
from app.database.schema import (
    CompanyInvoice,
    CompanyInvoiceExtra,
    Permission,
    Transaction,
    User,
    UserInvoice,
    UserInvoiceExtra,
)

from app.models import (
    CompanyInvoiceCreate,
    CompanyInvoiceExtraCreate,
    CompanyInvoiceExtraUpdate,
    UserInvoiceCreate,
    UserInvoiceExtraCreate,
    UserInvoiceExtraUpdate,
)
from app.responses import (
    create_user_invoice_extra_response,
    get_user_invoice_extra_response,
    update_user_invoice_extra_response,
    delete_user_invoice_extra_response,
    create_user_invoice_response,
    get_user_invoice_response,
    create_company_invoice_extra_response,
    get_company_invoice_extra_response,
    update_company_invoice_extra_response,
    delete_company_invoice_extra_response,
    create_company_invoice_response,
    get_company_invoice_response,
    get_monthly_cancel_fee_response,
    get_monthly_revenue_response,
    get_monthly_plate_fee_response,
    get_monthly_employee_salary_response,
)
from app.utils.auth import get_permission_info
from app.utils.jwt import auth_handler, authorization


router = APIRouter(prefix="/invoice")
true = True
false = False


@router.post("/user/extra", status_code=201, responses=create_user_invoice_extra_response())
def create_user_invoice_extra(
    request_info: UserInvoiceExtraCreate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `User invoice extra 생성 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{request_info.year}-{request_info.month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    is_extra_name_valid = validate_extra_name(request_info.name)
    if not is_extra_name_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_extra_name_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)

    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    user = User.get(session=session, id=request_info.user_id)
    if not user:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다."))

    if UserInvoiceExtra.get(
        session=session,
        user_id=request_info.user_id,
        year=int(request_info.year),
        month=int(request_info.month),
        name=request_info.name,
    ):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 존재하는 수당 이름입니다!"))

    try:
        created_object_id = UserInvoiceExtra.create(
            session=session,
            auto_commit=True,
            user_id=request_info.user_id,
            year=int(request_info.year),
            month=int(request_info.month),
            name=request_info.name,
            price=request_info.price,
        ).id
        return JSONResponse(
            status_code=201, content=dict(success=True, message="OK", result=dict(created_object_id=created_object_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.get("/user/extra", status_code=200, responses=get_user_invoice_extra_response())
def get_user_invoice_extra(
    user_id: Union[int, None] = None,
    year: str = None,
    month: str = None,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `User invoice extra 조회 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{year}-{month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice == "SR" and user_id is not None:
        if user_id != user_id_from_jwt:
            return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if user_id is None:
        user_id = user_id_from_jwt

    user = User.get(session=session, id=user_id)
    if not user:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다."))

    user_invoice_extra = (
        UserInvoiceExtra.filter(
            session=session,
            user_id=user_id,
            year=int(year),
            month=int(month),
            with_entities=[UserInvoiceExtra.id, UserInvoiceExtra.name, UserInvoiceExtra.price],
        )
        .order_by("id")
        .all()
    )

    result = {"success": True, "message": "OK", "result": user_invoice_extra}
    return result


@router.put("/user/extra/{extra_id}", status_code=200, responses=update_user_invoice_extra_response())
def update_user_invoice_extra(
    extra_id: int,
    request_info: UserInvoiceExtraUpdate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `User invoice extra 수정 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_extra_name_valid = validate_extra_name(request_info.name)
    if not is_extra_name_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_extra_name_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)

    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    user_invoice_extra = UserInvoiceExtra.get(session=session, id=extra_id)
    if not user_invoice_extra:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 수당입니다!"))

    if UserInvoiceExtra.get(
        session=session,
        user_id=user_invoice_extra.user_id,
        year=user_invoice_extra.year,
        month=user_invoice_extra.month,
        name=request_info.name,
    ):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 존재하는 수당 이름입니다!"))

    if UserInvoice.get(
        session=session,
        user_id=user_invoice_extra.user_id,
        year=user_invoice_extra.year,
        month=user_invoice_extra.month,
    ):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 정산이 완료되어 수정 또는 삭제가 불가능합니다!"))

    try:
        UserInvoiceExtra.filter(session=session, id=extra_id).update(
            auto_commit=True,
            name=request_info.name,
            price=request_info.price,
        )
        return JSONResponse(
            status_code=200, content=dict(success=True, message="OK", result=dict(updated_object_id=extra_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.delete("/user/extra/{extra_id}", status_code=200, responses=delete_user_invoice_extra_response())
def delete_user_invoice_extra(
    extra_id: int,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `User invoice extra 삭제 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
    if permission_info.transaction != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    user_invoice_extra = UserInvoiceExtra.get(session=session, id=extra_id)
    if not user_invoice_extra:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 수당입니다!"))

    if UserInvoice.get(
        session=session,
        user_id=user_invoice_extra.user_id,
        year=user_invoice_extra.year,
        month=user_invoice_extra.month,
    ):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 정산이 완료되어 수정 또는 삭제가 불가능합니다!"))

    try:
        UserInvoiceExtra.filter(session=session, id=extra_id).delete(auto_commit=True)
        return JSONResponse(
            status_code=200,
            content=dict(success=True, message="OK", result=dict(deleted_object_id=extra_id)),
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.post("/user", status_code=201, responses=create_user_invoice_response())
def create_user_invoice(
    request_info: UserInvoiceCreate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `User invoice 생성 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{request_info.year}-{request_info.month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    user = User.get(session=session, id=request_info.user_id)
    if not user:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다."))

    to_create = calculate_user_invoice(
        user=user, user_id=request_info.user_id, year=request_info.year, month=request_info.month, session=session
    )
    del to_create["extra"]

    try:
        created_object_id = UserInvoice.create(session=session, auto_commit=True, **to_create).id
        return JSONResponse(
            status_code=201, content=dict(success=True, message="OK", result=dict(created_object_id=created_object_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.get("/user", status_code=200, responses=get_user_invoice_response())
def get_user_invoice(
    user_id: Union[int, None] = None,
    year: str = None,
    month: str = None,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `User invoice 조회 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{year}-{month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice == "SR" and user_id is not None:
        if user_id != user_id_from_jwt:
            return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if user_id is None:
        user_id = user_id_from_jwt

    user = User.get(session=session, id=user_id)
    if not user:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정입니다."))

    user_invoice = UserInvoice.get(session=session, user_id=user_id, year=int(year), month=int(month))
    if user_invoice:
        user_invoice = jsonable_encoder(user_invoice)
        extra = (
            UserInvoiceExtra.filter(
                session=session,
                user_id=user_id,
                year=int(year),
                month=int(month),
                with_entities=[UserInvoiceExtra.name, UserInvoiceExtra.price],
            )
            .order_by("id")
            .all()
        )
        del user_invoice["created_at"]
        del user_invoice["updated_at"]
        user_invoice["extra"] = extra
        result = {"success": True, "message": "OK", "result": user_invoice}
        return result

    result = calculate_user_invoice(user=user, user_id=user_id, year=year, month=month, session=session)
    result = {"success": True, "message": "OK", "result": result}

    return result


@router.post("/company/extra", status_code=201, responses=create_company_invoice_extra_response())
def create_company_invoice_extra(
    request_info: CompanyInvoiceExtraCreate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `Company invoice extra 생성 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{request_info.year}-{request_info.month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    is_extra_name_valid = validate_extra_name(request_info.name)
    if not is_extra_name_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_extra_name_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)

    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if CompanyInvoiceExtra.get(
        session=session,
        year=int(request_info.year),
        month=int(request_info.month),
        name=request_info.name,
    ):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 존재하는 수당 이름입니다!"))

    try:
        created_object_id = CompanyInvoiceExtra.create(
            session=session,
            auto_commit=True,
            year=int(request_info.year),
            month=int(request_info.month),
            name=request_info.name,
            price=request_info.price,
        ).id
        return JSONResponse(
            status_code=201, content=dict(success=True, message="OK", result=dict(created_object_id=created_object_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.get("/company/extra", status_code=200, responses=get_company_invoice_extra_response())
def get_company_invoice_extra(
    year: str = None,
    month: str = None,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `Company invoice extra 조회 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{year}-{month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if "AR" not in permission_info.invoice:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    company_invoice_extra = (
        CompanyInvoiceExtra.filter(
            session=session,
            year=int(year),
            month=int(month),
            with_entities=[CompanyInvoiceExtra.id, CompanyInvoiceExtra.name, CompanyInvoiceExtra.price],
        )
        .order_by("id")
        .all()
    )

    result = {"success": True, "message": "OK", "result": company_invoice_extra}
    return result


@router.put("/company/extra/{extra_id}", status_code=200, responses=update_company_invoice_extra_response())
def update_company_invoice_extra(
    extra_id: int,
    request_info: CompanyInvoiceExtraUpdate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `Company invoice extra 수정 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_extra_name_valid = validate_extra_name(request_info.name)
    if not is_extra_name_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_extra_name_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)

    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    company_invoice_extra = CompanyInvoiceExtra.get(session=session, id=extra_id)
    if not company_invoice_extra:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 수당입니다!"))

    if CompanyInvoiceExtra.get(
        session=session,
        year=company_invoice_extra.year,
        month=company_invoice_extra.month,
        name=request_info.name,
    ):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 존재하는 수당 이름입니다!"))

    if CompanyInvoice.get(
        session=session,
        year=company_invoice_extra.year,
        month=company_invoice_extra.month,
    ):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 정산이 완료되어 수정 또는 삭제가 불가능합니다!"))

    try:
        CompanyInvoiceExtra.filter(session=session, id=extra_id).update(
            auto_commit=True,
            name=request_info.name,
            price=request_info.price,
        )
        return JSONResponse(
            status_code=200, content=dict(success=True, message="OK", result=dict(updated_object_id=extra_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.delete("/company/extra/{extra_id}", status_code=200, responses=delete_company_invoice_extra_response())
def delete_company_invoice_extra(
    extra_id: int,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `Company invoice extra 삭제 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
    if permission_info.transaction != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    company_invoice_extra = CompanyInvoiceExtra.get(session=session, id=extra_id)
    if not company_invoice_extra:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 수당입니다!"))

    if CompanyInvoice.get(
        session=session,
        year=company_invoice_extra.year,
        month=company_invoice_extra.month,
    ):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 정산이 완료되어 수정 또는 삭제가 불가능합니다!"))

    try:
        CompanyInvoiceExtra.filter(session=session, id=extra_id).delete(auto_commit=True)
        return JSONResponse(
            status_code=200,
            content=dict(success=True, message="OK", result=dict(deleted_object_id=extra_id)),
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.post("/company", status_code=201, responses=create_company_invoice_response())
def create_company_invoice(
    request_info: CompanyInvoiceCreate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `Company invoice 생성 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{request_info.year}-{request_info.month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    users = (
        session.query(
            User.id,
        )
        .join(Permission, User.id == Permission.user_id)
        .filter(
            User.status == "accepted",
            Permission.invoice != "ARW",
        )
    ).all()
    users = [user["id"] for user in users]
    count = UserInvoice.filter(
        session=session, year=int(request_info.year), month=int(request_info.month), user_id__in=users
    ).count()

    if len(users) != count:
        return JSONResponse(status_code=403, content=dict(success=False, message="모든 직원의 금월 급여가 정산된 이후에 조회 가능합니다!"))

    to_create = calculate_company_invoice(
        year=request_info.year,
        month=request_info.month,
        rental_fee=request_info.rental_fee,
        maintenance_fee=request_info.maintenance_fee,
        session=session,
    )
    del to_create["extra"]

    try:
        created_object_id = CompanyInvoice.create(session=session, auto_commit=True, **to_create).id
        return JSONResponse(
            status_code=201, content=dict(success=True, message="OK", result=dict(created_object_id=created_object_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.get("/company", status_code=200, responses=get_company_invoice_response())
def get_company_invoice(
    year: str = None,
    month: str = None,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `Company invoice 조회 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{year}-{month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    users = (
        session.query(
            User.id,
        )
        .join(Permission, User.id == Permission.user_id)
        .filter(
            User.status == "accepted",
            Permission.invoice != "ARW",
        )
    ).all()
    users = [user["id"] for user in users]
    count = UserInvoice.filter(session=session, year=int(year), month=int(month), user_id__in=users).count()

    if len(users) != count:
        return JSONResponse(status_code=403, content=dict(success=False, message="모든 직원의 금월 급여가 정산된 이후에 조회 가능합니다!"))

    company_invoice = CompanyInvoice.get(session=session, year=int(year), month=int(month))
    if company_invoice:
        company_invoice = jsonable_encoder(company_invoice)
        extra = (
            CompanyInvoiceExtra.filter(
                session=session,
                year=int(year),
                month=int(month),
                with_entities=[CompanyInvoiceExtra.name, CompanyInvoiceExtra.price],
            )
            .order_by("id")
            .all()
        )
        del company_invoice["created_at"]
        del company_invoice["updated_at"]
        company_invoice["extra"] = extra
        result = {"success": True, "message": "OK", "result": company_invoice}
        return result

    result = calculate_company_invoice(year=year, month=month, session=session)
    result = {"success": True, "message": "OK", "result": result}

    return result


@router.get("/monthly/cancel_fee", status_code=200, responses=get_monthly_cancel_fee_response())
def get_monthly_cancel_fee(
    year: str = None,
    month: str = None,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `월별 총 취소 수수료 조회 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{year}-{month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    start_date = f"{year}-{month}-01"
    end_date = f"{year}-{month}-{monthrange(int(year), int(month))[1]:02}"

    cancel_fee = (
        session.query(func.sum(Transaction.cancel_fee).label("cancel_fee"))
        .filter(
            Transaction.date.between(start_date, end_date),
            Transaction.canceled == true,
        )
        .first()
    )[0] or 0

    result = {"success": True, "message": "OK", "result": {"cancel_fee": cancel_fee}}

    return result


@router.get("/monthly/revenue", status_code=200, responses=get_monthly_revenue_response())
def get_monthly_revenue(
    year: str = None,
    month: str = None,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `월별 총 매출 조회 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{year}-{month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    start_date = f"{year}-{month}-01"
    end_date = f"{year}-{month}-{monthrange(int(year), int(month))[1]:02}"

    non_canceled_revenue = (
        session.query(func.sum(Transaction.price).label("non_canceled_revenue"))
        .filter(
            Transaction.date.between(start_date, end_date),
            Transaction.canceled == false,
        )
        .first()
    )[0] or 0

    canceled_revenue = (
        session.query(func.sum(Transaction.cancel_fee).label("canceled_revenue"))
        .filter(
            Transaction.date.between(start_date, end_date),
            Transaction.canceled == true,
        )
        .first()
    )[0] or 0

    revenue = non_canceled_revenue + canceled_revenue
    result = {"success": True, "message": "OK", "result": {"revenue": revenue}}

    return result


@router.get("/monthly/plate_fee", status_code=200, responses=get_monthly_plate_fee_response())
def get_monthly_plate_fee(
    year: str = None,
    month: str = None,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `월별 총 지입료 조회 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{year}-{month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    users = (
        session.query(
            User.id,
        )
        .join(Permission, User.id == Permission.user_id)
        .filter(
            User.status == "accepted",
            Permission.invoice != "ARW",
        )
    ).all()
    users = [user["id"] for user in users]
    count = UserInvoice.filter(session=session, year=int(year), month=int(month), user_id__in=users).count()

    if len(users) != count:
        return JSONResponse(status_code=403, content=dict(success=False, message="모든 직원의 금월 급여가 정산된 이후에 조회 가능합니다!"))

    plate_fee = (
        session.query(func.sum(UserInvoice.plate_fee).label("plate_fee"))
        .filter(
            UserInvoice.year == int(year),
            UserInvoice.month == int(month),
        )
        .first()
    )[0] or 0

    result = {"success": True, "message": "OK", "result": {"plate_fee": plate_fee}}

    return result


@router.get("/monthly/employee_salary", status_code=200, responses=get_monthly_employee_salary_response())
def get_monthly_employee_salary(
    year: str = None,
    month: str = None,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `월별 총 직원 급여 조회 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_date_valid = validate_date(f"{year}-{month}-01")
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.invoice != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    users = (
        session.query(
            User.id,
        )
        .join(Permission, User.id == Permission.user_id)
        .filter(
            User.status == "accepted",
            Permission.invoice != "ARW",
        )
    ).all()
    users = [user["id"] for user in users]
    count = UserInvoice.filter(session=session, year=int(year), month=int(month), user_id__in=users).count()

    if len(users) != count:
        return JSONResponse(status_code=403, content=dict(success=False, message="모든 직원의 금월 급여가 정산된 이후에 조회 가능합니다!"))

    employee_salary = (
        session.query(func.sum(UserInvoice.income).label("employee_salary"))
        .filter(
            UserInvoice.year == int(year),
            UserInvoice.month == int(month),
        )
        .first()
    )[0] or 0

    result = {"success": True, "message": "OK", "result": {"employee_salary": employee_salary}}

    return result


def calculate_user_invoice(
    user: User, user_id: int, year: str, month: str, session: Session = Depends(db.session)
) -> dict:
    start_date = f"{year}-{month}-01"
    end_date = f"{year}-{month}-{monthrange(int(year), int(month))[1]:02}"

    transaction_count = (
        session.query(func.count(Transaction.id).label("transaction_count"))
        .filter(
            Transaction.user_id == user_id,
            Transaction.date.between(start_date, end_date),
        )
        .first()
    )[0] or 0

    canceled_transaction_count = (
        session.query(func.count(Transaction.id).label("transaction_count"))
        .filter(
            Transaction.user_id == user_id,
            Transaction.canceled == true,
            Transaction.date.between(start_date, end_date),
        )
        .first()
    )[0] or 0

    revenue = (
        session.query(func.sum(Transaction.price).label("revenue"))
        .filter(
            Transaction.user_id == user_id,
            Transaction.date.between(start_date, end_date),
            Transaction.canceled == false,
        )
        .first()
    )[0] or 0

    cancel_fee = (
        session.query(func.sum(Transaction.cancel_fee).label("cancel_fee"))
        .filter(
            Transaction.user_id == user_id,
            Transaction.date.between(start_date, end_date),
            Transaction.canceled == true,
        )
        .first()
    )[0] or 0

    extra = UserInvoiceExtra.filter(
        session=session,
        user_id=user_id,
        year=int(year),
        month=int(month),
        with_entities=[UserInvoiceExtra.name, UserInvoiceExtra.price],
    ).all()

    contract_fee = user.contract_fee
    plate_fee = user.plate_fee
    total_revenue = revenue + cancel_fee
    total_contract_fee = int(float(total_revenue) * contract_fee * 0.01)
    first_vat = int(float(total_revenue - total_contract_fee) * 0.1)
    first_income = total_revenue - total_contract_fee + first_vat - plate_fee
    result = {
        "user_id": user_id,
        "contract_fee": contract_fee,
        "plate_fee": plate_fee,
        "year": year,
        "month": month,
        "transaction_count": transaction_count,
        "canceled_transaction_count": canceled_transaction_count,
        "revenue": revenue,
        "cancel_fee": cancel_fee,
        "total_revenue": total_revenue,
        "total_contract_fee": total_contract_fee,
        "first_vat": first_vat,
        "first_income": first_income,
        "extra": [],
        "second_vat": 0,
        "second_income": 0,
        "income": first_income,
    }

    if extra:
        extra_price = sum([x.price for x in extra])
        second_vat = int(float(first_income + extra_price) * 0.1)
        second_income = first_income + extra_price + second_vat
        result["extra"] = extra
        result["second_vat"] = second_vat
        result["second_income"] = second_income
        result["income"] = second_income

    return result


def calculate_company_invoice(
    year: str, month: str, rental_fee: int = None, maintenance_fee: int = None, session: Session = Depends(db.session)
) -> dict:
    start_date = f"{year}-{month}-01"
    end_date = f"{year}-{month}-{monthrange(int(year), int(month))[1]:02}"

    non_canceled_revenue = (
        session.query(func.sum(Transaction.price).label("non_canceled_revenue"))
        .filter(
            Transaction.date.between(start_date, end_date),
            Transaction.canceled == false,
        )
        .first()
    )[0] or 0

    canceled_revenue = (
        session.query(func.sum(Transaction.cancel_fee).label("canceled_revenue"))
        .filter(
            Transaction.date.between(start_date, end_date),
            Transaction.canceled == true,
        )
        .first()
    )[0] or 0

    revenue = non_canceled_revenue + canceled_revenue

    plate_fee = (
        session.query(func.sum(UserInvoice.plate_fee).label("plate_fee"))
        .filter(
            UserInvoice.year == int(year),
            UserInvoice.month == int(month),
        )
        .first()
    )[0] or 0

    employee_salary = (
        session.query(func.sum(UserInvoice.income).label("employee_salary"))
        .filter(
            UserInvoice.year == int(year),
            UserInvoice.month == int(month),
        )
        .first()
    )[0] or 0

    extra = CompanyInvoiceExtra.filter(
        session=session,
        year=int(year),
        month=int(month),
        with_entities=[CompanyInvoiceExtra.name, CompanyInvoiceExtra.price],
    ).all()

    result = {
        "year": year,
        "month": month,
        "revenue": revenue,
        "plate_fee": plate_fee,
        "employee_salary": employee_salary,
        "extra": [],
    }

    if extra:
        result["extra"] = extra

    if rental_fee:
        result["rental_fee"] = rental_fee

    if maintenance_fee:
        result["maintenance_fee"] = maintenance_fee

    if rental_fee is not None and maintenance_fee is not None:
        result["income"] = (revenue + plate_fee) - (employee_salary + rental_fee + maintenance_fee)
        if extra:
            extra_price = sum([x.price for x in extra])
            result["income"] += extra_price

    return result


def validate_date(date: str) -> dict:
    result = {"detail": "", "success": False}
    try:
        datetime.strptime(date, "%Y-%m-%d")
        result["detail"] = "OK"
        result["success"] = True
    except Exception as e:
        print(e)
        result["detail"] = "날짜 형식이 올바르지 않습니다!"
    return result


def validate_extra_name(memo: str) -> dict:
    result = {"detail": "", "success": False}
    if not (2 <= len(memo) <= 15):
        result["detail"] = "수당 이름은 2자 이상, 15자 이하여야 합니다!"
        return result
    else:
        result["detail"] = "OK"
        result["success"] = True
        return result
