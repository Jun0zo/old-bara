from calendar import monthrange
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import desc, cast, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, label

from app.database.conn import db
from app.database.schema import User, Transaction, UserInvoice, InsuranceCompany
from app.responses import (
    get_current_month_member_revenue_rate_response,
    get_current_month_insurance_company_rate_response,
    get_current_revenue_response,
    get_current_transaction_count_response,
    get_monthly_member_revenue_response,
    get_monthly_revenue_response,
)
from app.utils.auth import get_permission_info
from app.utils.date import get_now_datetime
from app.utils.jwt import auth_handler, authorization

router = APIRouter(prefix="/dashboard")
true = True
false = False


@router.get("/current-month-revenue", status_code=200, responses=get_current_revenue_response())
def get_current_month_revenue(
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    now = get_now_datetime()
    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    previous_start_date = (now - relativedelta(months=1)).strftime("%Y-%m-") + "01"
    previous_end_date = now - relativedelta(months=1)
    previous_end_date = (
        previous_end_date.strftime("%Y-%m-") + f"{monthrange(previous_end_date.year, previous_end_date.month)[1]:02}"
    )

    previous_non_canceled_revenue = (
        session.query(func.sum(Transaction.price).label("previous_non_canceled_revenue"))
        .filter(
            Transaction.date.between(previous_start_date, previous_end_date),
            Transaction.canceled == false,
        )
        .first()
    )[0] or 0

    previous_canceled_revenue = (
        session.query(func.sum(Transaction.cancel_fee).label("previous_canceled_revenue"))
        .filter(
            Transaction.date.between(previous_start_date, previous_end_date),
            Transaction.canceled == true,
        )
        .first()
    )[0] or 0

    previous_revenue = previous_non_canceled_revenue + previous_canceled_revenue

    current_non_canceled_revenue = (
        session.query(func.sum(Transaction.price).label("current_non_canceled_revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == false,
        )
        .first()
    )[0] or 0

    current_canceled_revenue = (
        session.query(func.sum(Transaction.cancel_fee).label("current_canceled_revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == true,
        )
        .first()
    )[0] or 0

    current_revenue = int(current_non_canceled_revenue) + int(current_canceled_revenue)

    difference_percentage = (
        round((current_revenue - previous_revenue) / previous_revenue * 100)
        if current_revenue - previous_revenue
        else 0
    )

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "revenue": current_revenue,
            "difference_percentage": difference_percentage,
        },
    }
    return result


@router.get("/current-day-revenue", status_code=200, responses=get_current_revenue_response())
def get_current_day_revenue(
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    now = get_now_datetime()
    current_day = now.strftime("%Y-%m-%d")

    previous_day = (now - relativedelta(days=1)).strftime("%Y-%m-%d")

    previous_non_canceled_revenue = (
        session.query(func.sum(Transaction.price).label("previous_non_canceled_revenue"))
        .filter(
            Transaction.date == previous_day,
            Transaction.canceled == false,
        )
        .first()
    )[0] or 0

    previous_canceled_revenue = (
        session.query(func.sum(Transaction.cancel_fee).label("previous_canceled_revenue"))
        .filter(
            Transaction.date == previous_day,
            Transaction.canceled == true,
        )
        .first()
    )[0] or 0

    previous_revenue = previous_non_canceled_revenue + previous_canceled_revenue

    current_non_canceled_revenue = (
        session.query(func.sum(Transaction.price).label("current_non_canceled_revenue"))
        .filter(
            Transaction.date == current_day,
            Transaction.canceled == false,
        )
        .first()
    )[0] or 0

    current_canceled_revenue = (
        session.query(func.sum(Transaction.cancel_fee).label("current_canceled_revenue"))
        .filter(
            Transaction.date == current_day,
            Transaction.canceled == true,
        )
        .first()
    )[0] or 0

    current_revenue = int(current_non_canceled_revenue) + int(current_canceled_revenue)

    difference_percentage = (
        round((current_revenue - previous_revenue) / previous_revenue * 100)
        if current_revenue - previous_revenue
        else 0
    )

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "revenue": current_revenue,
            "difference_percentage": difference_percentage,
        },
    }
    return result


@router.get("/current-month-transaction-count", status_code=200, responses=get_current_transaction_count_response())
def get_current_month_transaction_count(
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    now = get_now_datetime()
    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    previous_start_date = (now - relativedelta(months=1)).strftime("%Y-%m-") + "01"
    previous_end_date = now - relativedelta(months=1)
    previous_end_date = (
        previous_end_date.strftime("%Y-%m-") + f"{monthrange(previous_end_date.year, previous_end_date.month)[1]:02}"
    )

    previous_transaction_count = (
        session.query(func.count(Transaction.id).label("previous_transaction_count"))
        .filter(
            Transaction.date.between(previous_start_date, previous_end_date),
        )
        .first()
    )[0] or 0

    current_transaction_count = (
        session.query(func.count(Transaction.id).label("current_transaction_count"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
        )
        .first()
    )[0] or 0

    difference_count = int(current_transaction_count - previous_transaction_count)

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "transaction_count": current_transaction_count,
            "difference_count": difference_count,
        },
    }
    return result


@router.get("/current-day-transaction-count", status_code=200, responses=get_current_transaction_count_response())
def get_current_day_transaction_count(
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    now = get_now_datetime()
    current_day = now.strftime("%Y-%m-%d")

    previous_day = (now - relativedelta(days=1)).strftime("%Y-%m-%d")

    previous_transaction_count = (
        session.query(func.count(Transaction.id).label("previous_transaction_count"))
        .filter(
            Transaction.date == previous_day,
        )
        .first()
    )[0] or 0

    current_transaction_count = (
        session.query(func.count(Transaction.id).label("current_transaction_count"))
        .filter(
            Transaction.date == current_day,
        )
        .first()
    )[0] or 0

    difference_count = int(current_transaction_count - previous_transaction_count)

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "transaction_count": current_transaction_count,
            "difference_count": difference_count,
        },
    }
    return result


@router.get("/monthly-revenue/{month_range}", status_code=200, responses=get_monthly_revenue_response())
def get_monthly_revenue(
    month_range: int = 0,
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if month_range <= 0:
        return JSONResponse(status_code=400, content=dict(success=False, message="존재하지 않는 데이터입니다!"))

    now = get_now_datetime()
    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    current_non_canceled_revenue = int(
        (
            session.query(func.sum(Transaction.price).label("revenue"))
            .filter(
                Transaction.date.between(current_start_date, current_end_date),
                Transaction.canceled == false,
            )
            .first()
        )[0]
        or 0
    )
    current_canceled_revenue = int(
        (
            session.query(func.sum(Transaction.cancel_fee).label("revenue"))
            .filter(
                Transaction.date.between(current_start_date, current_end_date),
                Transaction.canceled == true,
            )
            .first()
        )[0]
        or 0
    )
    current_revenue = current_non_canceled_revenue + current_canceled_revenue
    current_revenue_obj = {
        "year": now.year,
        "month": now.month,
        "revenue": current_revenue,
    }

    revenue_list = []

    if month_range != 1:
        previous_start_date = now - relativedelta(months=month_range - 1)
        previous_end_date = now - relativedelta(months=1)

        last_date = (
            session.query(
                UserInvoice.year.label("year"),
                UserInvoice.month.label("month"),
            )
            .select_from(UserInvoice)
            .order_by(
                UserInvoice.year.label("year"),
                UserInvoice.month.label("month"),
            )
            .first()
        )

        if previous_start_date.year < last_date[0] and previous_start_date.month < last_date[1]:
            previous_start_date = datetime(last_date[0], last_date[1], 1)

        sub_query = (
            session.query(
                label("date", cast(UserInvoice.year, String) + "-" + cast(UserInvoice.month, String)),
                UserInvoice.year.label("year"),
                UserInvoice.month.label("month"),
                func.sum(UserInvoice.revenue).label("revenue"),
            )
            .group_by(
                UserInvoice.year,
                UserInvoice.month,
            )
            .subquery()
        )

        previous_revenue_list = (
            session.query(
                sub_query.c.year.label("year"),
                sub_query.c.month.label("month"),
                sub_query.c.revenue.label("revenue"),
            )
            .select_from(sub_query)
            .filter(
                sub_query.c.date.between(
                    f"{previous_start_date.year}-{previous_start_date.month}",
                    f"{previous_end_date.year}-{previous_end_date.month}",
                )
            )
            .order_by(
                sub_query.c.year,
                sub_query.c.month,
            )
            .all()
        )
        revenue_list = previous_revenue_list

    revenue_list.append(current_revenue_obj)
    result = {
        "success": True,
        "message": "OK",
        "result": {
            "revenue_list": revenue_list,
        },
    }

    return result


@router.get("/monthly-member-revenue", status_code=200, responses=get_monthly_member_revenue_response())
def get_monthly_member_revenue(
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    now = get_now_datetime()
    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    non_canceled_sub_query = (
        session.query(
            User.name.label("user_name"),
            User.id.label("user_id"),
            func.sum(Transaction.price).label("revenue"),
        )
        .select_from(Transaction)
        .join(User, User.id == Transaction.user_id)
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == false,
        )
        .group_by(User.name, User.id)
        .subquery()
    )

    user_list = (
        session.query(
            non_canceled_sub_query.c.user_name.label("user_name"),
            label("revenue", non_canceled_sub_query.c.revenue + func.sum(Transaction.cancel_fee)),
        )
        .select_from(Transaction)
        .outerjoin(non_canceled_sub_query, non_canceled_sub_query.c.user_id == Transaction.user_id)
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
        )
        .group_by(
            non_canceled_sub_query.c.user_name,
            non_canceled_sub_query.c.revenue,
        )
        .order_by(desc(label("revenue", non_canceled_sub_query.c.revenue + func.sum(Transaction.cancel_fee))))
        .all()
    )

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "user_list": user_list,
        },
    }
    return result


@router.get(
    "/current-month-member-revenue-rate", status_code=200, responses=get_current_month_member_revenue_rate_response()
)
def get_current_month_member_revenue_rate(
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    now = get_now_datetime()
    previous_date = now - relativedelta(months=1)

    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    previous_total_revenue = int(
        (
            session.query(func.sum(UserInvoice.revenue).label("revenue"))
            .filter(
                UserInvoice.year == previous_date.year,
                UserInvoice.month == previous_date.month,
            )
            .first()[0]
            or 0
        )
    )

    previous_percentage_sub_query = (
        session.query(
            User.name.label("user_name"),
            User.id.label("user_id"),
            label("percentage", cast(UserInvoice.revenue.label("revenue") / previous_total_revenue * 100, Integer)),
        )
        .select_from(UserInvoice)
        .outerjoin(
            User,
            User.id == UserInvoice.user_id,
        )
        .filter(
            UserInvoice.year == previous_date.year,
            UserInvoice.month == previous_date.month,
        )
        .group_by(
            User.name,
            User.id,
            UserInvoice.revenue,
        )
        .subquery()
    )

    current_total_price = int(
        (
            session.query(func.sum(Transaction.price).label("total_price"))
            .filter(Transaction.date.between(current_start_date, current_end_date), Transaction.canceled == false)
            .first()[0]
            or 0
        )
    )

    current_total_cancel_fee = int(
        (
            session.query(func.sum(Transaction.cancel_fee).label("total_cancel_fee"))
            .filter(
                Transaction.date.between(current_start_date, current_end_date),
                Transaction.canceled == true,
            )
            .first()[0]
            or 0
        )
    )

    current_total_revenue = current_total_price + current_total_cancel_fee

    current_sub_query = (
        session.query(
            User.name.label("user_name"),
            User.id.label("user_id"),
            func.sum(Transaction.price).label("revenue"),
        )
        .select_from(Transaction)
        .join(User, User.id == Transaction.user_id)
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == false,
        )
        .group_by(
            User.name,
            User.id,
        )
        .subquery()
    )

    current_percentage_sub_query = (
        session.query(
            current_sub_query.c.user_name.label("user_name"),
            current_sub_query.c.user_id.label("user_id"),
            label(
                "percentage",
                cast(
                    (current_sub_query.c.revenue + func.sum(Transaction.cancel_fee)) / current_total_revenue * 100,
                    Integer,
                ),
            ),
        )
        .select_from(Transaction)
        .outerjoin(
            current_sub_query,
            current_sub_query.c.user_id == Transaction.user_id,
        )
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == true,
        )
        .group_by(
            current_sub_query.c.user_name,
            current_sub_query.c.user_id,
            current_sub_query.c.revenue,
        )
        .subquery()
    )

    user_list = (
        session.query(
            current_percentage_sub_query.c.user_name.label("user_name"),
            current_percentage_sub_query.c.percentage.label("percentage"),
            label(
                "difference_percentage",
                current_percentage_sub_query.c.percentage - previous_percentage_sub_query.c.percentage,
            ),
        )
        .select_from(current_percentage_sub_query)
        .outerjoin(
            previous_percentage_sub_query,
            previous_percentage_sub_query.c.user_id == current_percentage_sub_query.c.user_id,
        )
        .group_by(
            current_percentage_sub_query.c.user_name,
            current_percentage_sub_query.c.percentage,
            previous_percentage_sub_query.c.percentage,
        )
        .order_by(desc(current_percentage_sub_query.c.percentage))
        .all()
    )

    result_user_list = []
    for user in user_list:
        user = user._asdict()
        user["percentage"] = int(user["percentage"]) if user["percentage"] else 0
        user["difference_percentage"] = int(user["difference_percentage"]) if user["difference_percentage"] else 0
        result_user_list.append(user)

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "user_list": result_user_list,
        },
    }

    return result


@router.get(
    "/current-month-invoice-company-rate",
    status_code=200,
    responses=get_current_month_insurance_company_rate_response(),
)
def get_current_month_insurance_company_rate(
    session: Session = Depends(db.session),
    jwt_token: HTTPAuthorizationCredentials = Security(authorization),
) -> JSONResponse:
    user_id_from_jwt = int(auth_handler.decode_token(token=jwt_token.credentials))

    permission_info = get_permission_info(session=session, user_id=user_id_from_jwt)
    if not permission_info:
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    if permission_info.user != "ARW":
        return JSONResponse(status_code=403, content=dict(success=False, message="권한이 없습니다!"))

    now = get_now_datetime()
    previous_start_date = (now - relativedelta(months=1)).strftime("%Y-%m-") + "01"
    previous_end_date = now - relativedelta(months=1)
    previous_end_date = (
        previous_end_date.strftime("%Y-%m-") + f"{monthrange(previous_end_date.year, previous_end_date.month)[1]:02}"
    )

    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    previous_transaction_count = int(
        (
            session.query(
                func.count(Transaction.id).label("transaction_count"),
            )
            .filter(Transaction.date.between(previous_start_date, previous_end_date))
            .first()[0]
            or 0
        )
    )

    previous_company_sub_query = (
        session.query(
            InsuranceCompany.name.label("company_name"),
            label("percentage", cast(func.count(Transaction.id) / previous_transaction_count * 100, Integer)),
        )
        .select_from(Transaction)
        .join(
            InsuranceCompany,
            InsuranceCompany.id == Transaction.insurance_company_id,
        )
        .filter(Transaction.date.between(previous_start_date, previous_end_date))
        .group_by(InsuranceCompany.name)
        .subquery()
    )

    current_transaction_count = int(
        (
            session.query(
                func.count(Transaction.id).label("transaction_count"),
            )
            .filter(Transaction.date.between(current_start_date, current_end_date))
            .first()[0]
            or 0
        )
    )

    current_company_sub_query = (
        session.query(
            InsuranceCompany.name.label("company_name"),
            label("percentage", cast(func.count(Transaction.id) / current_transaction_count * 100, Integer)),
        )
        .select_from(Transaction)
        .join(
            InsuranceCompany,
            InsuranceCompany.id == Transaction.insurance_company_id,
        )
        .filter(Transaction.date.between(current_start_date, current_end_date))
        .group_by(InsuranceCompany.name)
        .subquery()
    )

    company_list = (
        session.query(
            current_company_sub_query.c.company_name.label("company_name"),
            current_company_sub_query.c.percentage.label("percentage"),
            label(
                "difference_percentage",
                current_company_sub_query.c.percentage - previous_company_sub_query.c.percentage,
            ),
        )
        .select_from(current_company_sub_query)
        .outerjoin(
            previous_company_sub_query,
            previous_company_sub_query.c.company_name == current_company_sub_query.c.company_name,
        )
        .group_by(current_company_sub_query.c.company_name.label("company_name"))
        .order_by(
            desc(
                label(
                    "difference_percentage",
                    current_company_sub_query.c.percentage - previous_company_sub_query.c.percentage,
                )
            )
        )
        .all()
    )

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "company_list": company_list,
        },
    }
    return result
