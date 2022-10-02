from datetime import datetime
import re

from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.database.conn import db
from app.database.schema import InsuranceCompany, Transaction, User
from app.models import (
    InsuranceCompanyCreate,
    InsuranceCompanyUpdate,
    TransactionCreate,
    TransactionUpdate,
    TransactionTable,
)
from app.responses import (
    create_insurance_company_response,
    get_all_insurance_company_response,
    get_specific_insurance_company_response,
    update_insurance_company_response,
    delete_insurance_company_response,
    create_transaction_response,
    get_transaction_table_response,
    get_specific_transaction_response,
    update_transaction_response,
    delete_transaction_response,
)
from app.utils.auth import get_permission_info
from app.utils.jwt import auth_handler, authorization


router = APIRouter(prefix="/transaction")
true = True
false = False


@router.post("/insurancecompany", status_code=201, responses=create_insurance_company_response())
def create_insurance_company(
    request_info: InsuranceCompanyCreate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `보험사 생성 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_company_name_valid = validate_company_name(request_info.name)
    if not is_company_name_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_company_name_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)

    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.transaction != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if InsuranceCompany.get(session=session, name=request_info.name):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 존재하는 회사입니다!"))

    try:
        created_object_id = InsuranceCompany.create(session=session, auto_commit=True, name=request_info.name).id
        return JSONResponse(
            status_code=201, content=dict(success=True, message="OK", result=dict(created_object_id=created_object_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.get("/insurancecompany", status_code=200, responses=get_all_insurance_company_response())
def get_all_insurance_company(
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `모든 보험사 정보 받아오는 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    insurance_companies = (
        InsuranceCompany.filter(session=session, with_entities=[InsuranceCompany.id, InsuranceCompany.name])
        .order_by("id")
        .all()
    )
    result = {"success": True, "message": "OK", "result": insurance_companies}
    return result


@router.get(
    "/insurancecompany/{insurance_company_id}", status_code=200, responses=get_specific_insurance_company_response()
)
def get_specific_insurance_company(
    insurance_company_id: int,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `특정 보험사 정보 받아오는 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    insurance_company = InsuranceCompany.get(
        session=session, id=insurance_company_id, with_entities=[InsuranceCompany.id, InsuranceCompany.name]
    )
    if not insurance_company:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 보험사입니다!"))

    result = {"success": True, "message": "OK", "result": insurance_company}
    return result


@router.put("/insurancecompany/{insurance_company_id}", status_code=200, responses=update_insurance_company_response())
def update_insurance_company(
    insurance_company_id: int,
    request_info: InsuranceCompanyUpdate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `보험사 수정 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_company_name_valid = validate_company_name(request_info.name)
    if not is_company_name_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_company_name_valid["detail"]))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
    if permission_info.transaction != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if not InsuranceCompany.get(session=session, id=insurance_company_id):
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 보험사입니다!"))

    if InsuranceCompany.get(session=session, name=request_info.name):
        return JSONResponse(status_code=400, content=dict(success=False, message="이미 존재하는 보험사입니다!"))

    try:
        InsuranceCompany.filter(session=session, id=insurance_company_id).update(
            auto_commit=True, name=request_info.name
        )
        return JSONResponse(
            status_code=200,
            content=dict(success=True, message="OK", result=dict(updated_object_id=insurance_company_id)),
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.delete(
    "/insurancecompany/{insurance_company_id}", status_code=200, responses=delete_insurance_company_response()
)
def delete_insurance_company(
    insurance_company_id: int,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `보험사 삭제 API`
    """
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
    if permission_info.transaction != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if not InsuranceCompany.get(session=session, id=insurance_company_id):
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 보험사입니다!"))

    if Transaction.get(session=session, insurance_company_id=insurance_company_id):
        return JSONResponse(
            status_code=400,
            content=dict(
                success=False, message="해당 보험사와 발생한 거래가 1건 이상 존재합니다!\n" + "데이터 무결성을 위해 거래가 존재하는 보험사는 삭제할 수 없습니다!"
            ),
        )

    try:
        InsuranceCompany.filter(session=session, id=insurance_company_id).delete(auto_commit=True)
        return JSONResponse(
            status_code=200,
            content=dict(success=True, message="OK", result=dict(deleted_object_id=insurance_company_id)),
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.post("", status_code=201, responses=create_transaction_response())
def create_transaction(
    request_info: TransactionCreate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `거래 생성 API`
    """

    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    is_vehicle_id_valid = validate_vehicle_id(request_info.vehicle_id)
    if not is_vehicle_id_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_vehicle_id_valid["detail"]))

    is_vehicle_model_valid = validate_vehicle_model(request_info.vehicle_model)
    if not is_vehicle_model_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_vehicle_model_valid["detail"]))

    is_date_valid = validate_date(request_info.date)
    if not is_date_valid["success"]:
        return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))

    if request_info.memo is not None:
        is_memo_valid = validate_memo(request_info.date)
        if not is_memo_valid["success"]:
            return JSONResponse(status_code=400, content=dict(success=False, message=is_memo_valid["detail"]))
    else:
        request_info.memo = ""

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.transaction == "AR":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if request_info.user_id is not None:
        if permission_info.transaction == "SRW":
            return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
        if not User.get(session=session, id=request_info.user_id, status="accepted"):
            return JSONResponse(
                status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정이 거래 담당자로 지정되었습니다!")
            )
    else:
        request_info.user_id = user_id_from_jwt

    if not InsuranceCompany.get(session=session, id=request_info.insurance_company_id):
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 보험사입니다!"))

    try:
        created_object_id = Transaction.create(
            session=session,
            auto_commit=True,
            user_id=request_info.user_id,
            insurance_company_id=request_info.insurance_company_id,
            vehicle_id=request_info.vehicle_id,
            vehicle_model=request_info.vehicle_model,
            date=request_info.date,
            price=request_info.price,
            memo=request_info.memo,
        ).id
        return JSONResponse(
            status_code=201, content=dict(success=True, message="OK", result=dict(created_object_id=created_object_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.post("/table", status_code=200, responses=get_transaction_table_response())
def get_transaction_table(
    request_info: TransactionTable,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `거래 테이블 조회 API`
    """

    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if request_info.user_id is not None:
        if permission_info.transaction == "SRW":
            return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
        else:
            if not User.filter(session=session, id=request_info.user_id, status__in=["accepted", "deleted"]).first():
                return JSONResponse(status_code=400, content=dict(success=False, message="조회 대상 계정은 존재하지 않거나 탈퇴되었습니다!"))
    else:
        if permission_info.transaction == "SRW":
            request_info.user_id = user_id_from_jwt

    start_date = request_info.start_date
    end_date = request_info.end_date
    user_id = request_info.user_id
    insurance_company_id = request_info.insurance_company_id
    page = request_info.page
    limit = request_info.limit
    canceled_type = request_info.canceled_type
    order_by = request_info.order_by
    order_type = request_info.order_type

    order_by_dict = {
        "transaction_id": Transaction.id,
        "user_id": User.id,
        "price": Transaction.price,
        "cancel_fee": Transaction.cancel_fee,
    }

    order_by = order_by_dict[order_by]
    order_by = desc(order_by) if order_type == "desc" else asc(order_by)

    main_query = (
        session.query(
            Transaction.id,
            Transaction.date,
            Transaction.created_at,
            InsuranceCompany.name.label("insurance_company_name"),
            Transaction.vehicle_id,
            Transaction.vehicle_model,
            User.name.label("user_name"),
            Transaction.price,
            Transaction.memo,
            Transaction.canceled,
            Transaction.cancel_fee,
        )
        .join(InsuranceCompany, Transaction.insurance_company_id == InsuranceCompany.id)
        .join(User, Transaction.user_id == User.id)
    )

    if start_date is not None and end_date is not None:
        for date in [start_date, end_date]:
            is_date_valid = validate_date(date)
            if not is_date_valid["success"]:
                return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))
        if start_date > end_date:
            return JSONResponse(status_code=400, content=dict(success=False, message="조회 기간 설정이 올바르지 않습니다!"))
        main_query = main_query.filter(Transaction.date.between(start_date, end_date))

    if user_id is not None:
        main_query = main_query.filter(User.id == user_id)

    if insurance_company_id is not None:
        if not InsuranceCompany.get(session=session, id=insurance_company_id):
            return JSONResponse(status_code=400, content=dict(success=False, message="조회 대상 보험사가 존재하지 않습니다!"))
        main_query = main_query.filter(InsuranceCompany.id == insurance_company_id)

    if canceled_type == "EXCLUDE_CANCELED":
        main_query = main_query.filter(Transaction.canceled == false)
    elif canceled_type == "CANCELED_ONLY":
        main_query = main_query.filter(Transaction.canceled == true)

    total_length = main_query.count()
    transaction_list = main_query.order_by(order_by).offset(page * limit).limit(limit).all()

    result = {
        "success": True,
        "message": "OK",
        "result": {"total_length": total_length, "transaction_list": transaction_list},
    }
    return result


@router.get("/{transaction_id}", status_code=200, responses=get_specific_transaction_response())
def get_specific_transaction(
    transaction_id: int,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `특정 거래 조회 API`
    """

    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    transaction = Transaction.get(session=session, id=transaction_id)
    if not transaction:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 거래입니다!"))

    if transaction.user_id != user_id_from_jwt and permission_info.transaction == "SRW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    transaction = (
        session.query(
            Transaction.id,
            Transaction.date,
            Transaction.created_at,
            InsuranceCompany.name.label("insurance_company_name"),
            User.name.label("user_name"),
            Transaction.price,
            Transaction.vehicle_id,
            Transaction.vehicle_model,
            Transaction.memo,
            Transaction.canceled,
            Transaction.cancel_fee,
        )
        .join(InsuranceCompany, Transaction.insurance_company_id == InsuranceCompany.id)
        .join(User, Transaction.user_id == User.id)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    result = {"success": True, "message": "OK", "result": transaction}
    return result


@router.put("/{transaction_id}", status_code=200, responses=update_transaction_response())
def update_transaction(
    transaction_id: int,
    request_info: TransactionUpdate,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `거래 수정 API`
    """

    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    transaction = Transaction.get(session=session, id=transaction_id)
    if not transaction:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 거래입니다!"))

    if permission_info.transaction == "SRW":
        if transaction.user_id != user_id_from_jwt:
            return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    to_update_at = {}

    if request_info.user_id is not None:
        if permission_info.transaction == "SRW":
            return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))
        if not User.get(session=session, id=request_info.user_id, status="accepted"):
            return JSONResponse(
                status_code=400, content=dict(success=False, message="존재하지 않거나 탈퇴된 계정이 거래 담당자로 지정되었습니다!")
            )
        to_update_at["user_id"] = request_info.user_id

    if request_info.insurance_company_id is not None:
        if not InsuranceCompany.get(session=session, id=request_info.insurance_company_id):
            return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 보험사입니다!"))
        to_update_at["insurance_company_id"] = request_info.insurance_company_id

    if request_info.vehicle_id is not None:
        is_vehicle_id_valid = validate_vehicle_id(request_info.vehicle_id)
        if not is_vehicle_id_valid["success"]:
            return JSONResponse(status_code=400, content=dict(success=False, message=is_vehicle_id_valid["detail"]))
        to_update_at["vehicle_id"] = request_info.vehicle_id

    if request_info.vehicle_model is not None:
        is_vehicle_model_valid = validate_vehicle_model(request_info.vehicle_model)
        if not is_vehicle_model_valid["success"]:
            return JSONResponse(status_code=400, content=dict(success=False, message=is_vehicle_model_valid["detail"]))
        to_update_at["vehicle_model"] = request_info.vehicle_model

    if request_info.date is not None:
        is_date_valid = validate_date(request_info.date)
        if not is_date_valid["success"]:
            return JSONResponse(status_code=400, content=dict(success=False, message=is_date_valid["detail"]))
        to_update_at["date"] = request_info.date

    if request_info.memo is not None:
        is_memo_valid = validate_memo(request_info.memo)
        if not is_date_valid["success"]:
            return JSONResponse(status_code=400, content=dict(success=False, message=is_memo_valid["detail"]))
        to_update_at["memo"] = request_info.memo

    if request_info.canceled is not None:
        to_update_at["canceled"] = request_info.canceled
        if request_info.canceled:
            if request_info.cancel_fee is None:
                return JSONResponse(status_code=400, content=dict(success=False, message="취소 수수료를 입력해 주세요!"))
            if request_info.cancel_fee == 0:
                return JSONResponse(status_code=400, content=dict(success=False, message="취소 수수료는 0원일 수 없습니다!"))
            to_update_at["cancel_fee"] = request_info.cancel_fee
        else:
            to_update_at["cancel_fee"] = 0

    if not to_update_at:
        return JSONResponse(status_code=400, content=dict(success=False, message="수정할 값을 입력해 주세요!"))

    try:
        Transaction.filter(session=session, id=transaction_id).update(auto_commit=True, **to_update_at)
        return JSONResponse(
            status_code=200, content=dict(success=True, message="OK", result=dict(updated_object_id=transaction_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


@router.delete("/{transaction_id}", status_code=200, responses=delete_transaction_response())
def delete_transaction(
    transaction_id: int,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    """
    `거래 삭제 API`
    """

    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    transaction = Transaction.get(session=session, id=transaction_id)
    if not transaction:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 거래입니다!"))

    if permission_info.transaction != "ARW" and user_id_from_jwt != transaction.user_id:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    try:
        Transaction.filter(session=session, id=transaction_id).delete(auto_commit=True)
        return JSONResponse(
            status_code=200, content=dict(success=True, message="OK", result=dict(deleted_object_id=transaction_id))
        )
    except Exception as e:
        print(e)
        return JSONResponse(status_code=409, content=dict(success=False, message="예상치 못한 오류가 발생했습니다!"))


def validate_company_name(name: str) -> dict:
    result = {"detail": "", "success": False}
    if not (2 <= len(name) <= 10):
        result["detail"] = "사명은 2자 이상, 10자 이하여야 합니다!"
        return result

    elif " " in name:
        result["detail"] = "사명에는 공백이 포함될 수 없습니다!"
        return result

    elif re.search("[`~!@#$%^&*.?]+", name):
        result["detail"] = "사명에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"
        return result

    else:
        result["detail"] = "OK"
        result["success"] = True
        return result


def validate_vehicle_id(vehicle_id: str) -> dict:
    result = {"detail": "", "success": False}
    if not (4 <= len(vehicle_id) <= 10):
        result["detail"] = "차량번호는 4자 이상, 10자 이하여야 합니다!"
        return result

    elif re.search("[`~!@#$%^&*.?]+", vehicle_id):
        result["detail"] = "차량번호에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"
        return result

    elif any(c.encode().isalpha() for c in vehicle_id):
        result["detail"] = "차량번호에는 알파벳이 포함될 수 없습니다!"
        return result

    else:
        result["detail"] = "OK"
        result["success"] = True
        return result


def validate_vehicle_model(vehicle_model: str) -> dict:
    result = {"detail": "", "success": False}
    if not (2 <= len(vehicle_model) <= 10):
        result["detail"] = "차종은 2자 이상, 10자 이하여야 합니다!"
        return result

    elif re.search("[`~!@#$%^&*.?]+", vehicle_model):
        result["detail"] = "차종에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"
        return result

    else:
        result["detail"] = "OK"
        result["success"] = True
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


def validate_memo(memo: str) -> dict:
    result = {"detail": "", "success": False}
    if not (2 <= len(memo) <= 10):
        result["detail"] = "비고는 2자 이상, 10자 이하여야 합니다!"
        return result
    else:
        result["detail"] = "OK"
        result["success"] = True
        return result
