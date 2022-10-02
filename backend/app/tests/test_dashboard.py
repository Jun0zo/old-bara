from calendar import monthrange
from dataclasses import asdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from uuid import uuid4

import bcrypt
from fastapi.testclient import TestClient
from sqlalchemy import desc, cast, Integer, String
from sqlalchemy.sql import func, label

from app.common.config import conf
from app.database.conn import db, Base
from app.database.schema import (
    Permission,
    InsuranceCompany,
    Transaction,
    User,
    UserRole,
    UserInvoice,
)
from app.main import app
from app.tests.create_expired_jwt import create_expired_jwt
from app.utils.jwt import auth_handler
from app.utils.date import get_now_datetime
from app.utils.create_dummy_data import create_dummy_data

true = True
false = False


def create_test_users(session):
    UserRole.create(session=session, auto_commit=True, name="대표")
    User.create(
        session=session,
        auto_commit=True,
        email="admin@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김대표",
        role_id=UserRole.get(session=session, name="대표").id,
        status="accepted",
        plate_fee=1234,
        contract_fee=12.34,
    )
    Permission.create(
        session=session,
        auto_commit=True,
        user_id=User.get(session=session, email="admin@baraman.net").id,
        user="ARW",
        transaction="ARW",
        compensation="ARW",
    )

    UserRole.create(session=session, auto_commit=True, name="기사0")
    User.create(
        session=session,
        auto_commit=True,
        email="driver@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김기사",
        role_id=UserRole.get(session=session, name="기사0").id,
        status="accepted",
        plate_fee=5678,
        contract_fee=56.78,
    )
    Permission.create(
        session=session,
        auto_commit=True,
        user_id=User.get(session=session, email="driver@baraman.net").id,
        user="SR",
        transaction="SRW",
        compensation="SR",
    )


def create_test_JWT(user_id: str) -> str:
    return auth_handler.encode_token(subject=str(user_id))


def test_get_current_month_revenue():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/dashboard/current-month-revenue", headers={"Authorization": f"Bearer {token}"})

    now = get_now_datetime()
    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    previous_start_date = (now - relativedelta(months=1)).strftime("%Y-%m-") + "01"
    previous_end_date = now - relativedelta(months=1)
    previous_end_date = (
        previous_end_date.strftime("%Y-%m-") + f"{monthrange(previous_end_date.year, previous_end_date.month)[1]:02}"
    )

    previous_non_canceled_revenue = int(
        session.query(func.sum(Transaction.price).label("previous_non_canceled_revenue"))
        .filter(
            Transaction.date.between(previous_start_date, previous_end_date),
            Transaction.canceled == false,
        )
        .first()[0]
        or 0
    )

    previous_canceled_revenue = int(
        session.query(func.sum(Transaction.cancel_fee).label("previous_canceled_revenue"))
        .filter(
            Transaction.date.between(previous_start_date, previous_end_date),
            Transaction.canceled == true,
        )
        .first()[0]
        or 0
    )

    previous_revenue = previous_non_canceled_revenue + previous_canceled_revenue

    current_non_canceled_revenue = int(
        session.query(func.sum(Transaction.price).label("current_non_canceled_revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == false,
        )
        .first()[0]
        or 0
    )

    current_canceled_revenue = int(
        session.query(func.sum(Transaction.cancel_fee).label("current_canceled_revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == true,
        )
        .first()[0]
        or 0
    )

    current_revenue = current_non_canceled_revenue + current_canceled_revenue

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

    assert response.status_code == 200
    assert response.json() == result


def test_get_current_month_revenue_without_JWT():
    response = client.get("/api/dashboard/current-month-revenue")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_current_month_revenue_expired_JWT():
    token = expired_token

    response = client.get("/api/dashboard/current-month-revenue", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_current_month_revenue_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/dashboard/current-month-revenue", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_current_day_revenue():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/dashboard/current-day-revenue", headers={"Authorization": f"Bearer {token}"})

    now = get_now_datetime()
    current_day = now.strftime("%Y-%m-%d")

    previous_day = (now - relativedelta(days=1)).strftime("%Y-%m-%d")

    previous_non_canceled_revenue = int(
        session.query(func.sum(Transaction.price).label("previous_non_canceled_revenue"))
        .filter(
            Transaction.date == previous_day,
            Transaction.canceled == false,
        )
        .first()[0]
        or 0
    )

    previous_canceled_revenue = int(
        session.query(func.sum(Transaction.cancel_fee).label("previous_canceled_revenue"))
        .filter(
            Transaction.date == previous_day,
            Transaction.canceled == true,
        )
        .first()[0]
        or 0
    )

    previous_revenue = previous_non_canceled_revenue + previous_canceled_revenue

    current_non_canceled_revenue = int(
        session.query(func.sum(Transaction.price).label("current_non_canceled_revenue"))
        .filter(
            Transaction.date == current_day,
            Transaction.canceled == false,
        )
        .first()[0]
        or 0
    )

    current_canceled_revenue = int(
        session.query(func.sum(Transaction.cancel_fee).label("current_canceled_revenue"))
        .filter(
            Transaction.date == current_day,
            Transaction.canceled == true,
        )
        .first()[0]
        or 0
    )

    current_revenue = current_non_canceled_revenue + current_canceled_revenue

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

    assert response.status_code == 200
    assert response.json() == result


def test_get_current_day_revenue_without_JWT():
    response = client.get("/api/dashboard/current-day-revenue")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_current_day_revenue_expired_JWT():
    token = expired_token

    response = client.get("/api/dashboard/current-day-revenue", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_current_day_revenue_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/dashboard/current-day-revenue", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_current_month_transaction_count():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get(
        "/api/dashboard/current-month-transaction-count", headers={"Authorization": f"Bearer {token}"}
    )

    now = get_now_datetime()
    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    previous_start_date = (now - relativedelta(months=1)).strftime("%Y-%m-") + "01"
    previous_end_date = now - relativedelta(months=1)
    previous_end_date = (
        previous_end_date.strftime("%Y-%m-") + f"{monthrange(previous_end_date.year, previous_end_date.month)[1]:02}"
    )

    previous_transaction_count = int(
        session.query(func.count(Transaction.id).label("previous_transaction_count"))
        .filter(
            Transaction.date.between(previous_start_date, previous_end_date),
        )
        .first()[0]
        or 0
    )

    current_transaction_count = int(
        session.query(func.count(Transaction.id).label("current_transaction_count"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
        )
        .first()[0]
        or 0
    )

    difference_count = current_transaction_count - previous_transaction_count

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "transaction_count": current_transaction_count,
            "difference_count": difference_count,
        },
    }
    assert response.status_code == 200
    assert response.json() == result


def test_get_current_month_transaction_count_without_JWT():
    response = client.get("/api/dashboard/current-month-transaction-count")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_current_month_transaction_count_expired_JWT():
    token = expired_token

    response = client.get(
        "/api/dashboard/current-month-transaction-count", headers={"Authorization": f"Bearer {token}"}
    )

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_current_month_transaction_count_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get(
        "/api/dashboard/current-month-transaction-count", headers={"Authorization": f"Bearer {token}"}
    )

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_monthly_revenue_with_one_month():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/dashboard/monthly-revenue/1", headers={"Authorization": f"Bearer {token}"})

    now = get_now_datetime()
    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    current_non_canceled_revenue = int(
        session.query(func.sum(Transaction.price).label("revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == false,
        )
        .first()[0]
        or 0
    )
    current_canceled_revenue = int(
        session.query(func.sum(Transaction.cancel_fee).label("revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == true,
        )
        .first()[0]
        or 0
    )
    current_revenue = current_non_canceled_revenue + current_canceled_revenue
    current_revenue_obj = {
        "year": now.year,
        "month": now.month,
        "revenue": current_revenue,
    }

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "revenue_list": [current_revenue_obj],
        },
    }

    assert response.status_code == 200
    assert response.json() == result


def test_get_monthly_revenue_with_months():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    month_range = 3
    response = client.get(f"/api/dashboard/monthly-revenue/{month_range}", headers={"Authorization": f"Bearer {token}"})

    now = get_now_datetime()
    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    current_non_canceled_revenue = int(
        session.query(func.sum(Transaction.price).label("revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == false,
        )
        .first()[0]
        or 0
    )
    current_canceled_revenue = int(
        session.query(func.sum(Transaction.cancel_fee).label("revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == true,
        )
        .first()[0]
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
        for revenue in previous_revenue_list:
            revenue = revenue._asdict()
            revenue["year"] = int(revenue["year"])
            revenue["month"] = int(revenue["month"])
            revenue["revenue"] = int(revenue["revenue"]) if revenue["revenue"] else 0
            revenue_list.append(revenue)

    revenue_list.append(current_revenue_obj)

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "revenue_list": revenue_list,
        },
    }

    assert response.status_code == 200
    assert response.json() == result


def test_get_monthly_revenue_with_many_months():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    month_range = 3
    response = client.get(f"/api/dashboard/monthly-revenue/{month_range}", headers={"Authorization": f"Bearer {token}"})

    now = get_now_datetime()
    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    current_non_canceled_revenue = int(
        session.query(func.sum(Transaction.price).label("revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == false,
        )
        .first()[0]
        or 0
    )
    current_canceled_revenue = int(
        session.query(func.sum(Transaction.cancel_fee).label("revenue"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == true,
        )
        .first()[0]
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
        for revenue in previous_revenue_list:
            revenue = revenue._asdict()
            revenue["year"] = int(revenue["year"])
            revenue["month"] = int(revenue["month"])
            revenue["revenue"] = int(revenue["revenue"]) if revenue["revenue"] else 0
            revenue_list.append(revenue)

    revenue_list.append(current_revenue_obj)

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "revenue_list": revenue_list,
        },
    }

    assert response.status_code == 200
    assert response.json() == result


def test_get_monthly_revenue_invalid_month():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/dashboard/monthly-revenue/-1", headers={"Authorization": f"Bearer {token}"})

    result = {
        "success": False,
        "message": "존재하지 않는 데이터입니다!",
    }

    assert response.status_code == 400
    assert response.json() == result


def test_get_monthly_revenue_without_JWT():
    response = client.get("/api/dashboard/monthly-revenue/1")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_monthly_revenue_expired_JWT():
    token = expired_token

    response = client.get("/api/dashboard/monthly-revenue/1", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_monthly_revenue_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/dashboard/monthly-revenue/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_monthly_member_revenue():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/dashboard/monthly-member-revenue", headers={"Authorization": f"Bearer {token}"})

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

    result_user_list = []
    for revenue in user_list:
        revenue = revenue._asdict()
        revenue["revenue"] = int(revenue["revenue"]) if revenue["revenue"] else 0
        result_user_list.append(revenue)

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "user_list": result_user_list,
        },
    }

    assert response.status_code == 200
    assert response.json() == result


def test_get_monthly_member_revenue_without_JWT():
    response = client.get("/api/dashboard/monthly-member-revenue")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_monthly_member_revenue_expired_JWT():
    token = expired_token

    response = client.get("/api/dashboard/monthly-member-revenue", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_monthly_member_revenue_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/dashboard/monthly-member-revenue", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_current_month_member_revenue_rate():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get(
        "/api/dashboard/current-month-member-revenue-rate", headers={"Authorization": f"Bearer {token}"}
    )

    now = get_now_datetime()
    previous_date = now - relativedelta(months=1)

    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    previous_total_revenue = int(
        session.query(func.sum(UserInvoice.revenue).label("revenue"))
        .filter(
            UserInvoice.year == previous_date.year,
            UserInvoice.month == previous_date.month,
        )
        .first()[0]
        or 0
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
        session.query(func.sum(Transaction.price).label("total_price"))
        .filter(Transaction.date.between(current_start_date, current_end_date), Transaction.canceled == false)
        .first()[0]
        or 0
    )

    current_total_cancel_fee = int(
        session.query(func.sum(Transaction.cancel_fee).label("total_cancel_fee"))
        .filter(
            Transaction.date.between(current_start_date, current_end_date),
            Transaction.canceled == true,
        )
        .first()[0]
        or 0
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

    assert response.status_code == 200
    assert response.json() == result


def test_get_current_month_member_revenue_rate_without_JWT():
    response = client.get("/api/dashboard/current-month-member-revenue-rate")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_current_month_member_revenue_rate_expired_JWT():
    token = expired_token

    response = client.get(
        "/api/dashboard/current-month-member-revenue-rate", headers={"Authorization": f"Bearer {token}"}
    )

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_current_month_member_revenue_rate_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get(
        "/api/dashboard/current-month-member-revenue-rate", headers={"Authorization": f"Bearer {token}"}
    )

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_current_month_insurance_company_rate():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get(
        "/api/dashboard/current-month-invoice-company-rate", headers={"Authorization": f"Bearer {token}"}
    )

    now = get_now_datetime()
    previous_start_date = (now - relativedelta(months=1)).strftime("%Y-%m-") + "01"
    previous_end_date = now - relativedelta(months=1)
    previous_end_date = (
        previous_end_date.strftime("%Y-%m-") + f"{monthrange(previous_end_date.year, previous_end_date.month)[1]:02}"
    )

    current_start_date = now.strftime("%Y-%m-") + "01"
    current_end_date = now.strftime("%Y-%m-%d")

    previous_transaction_count = int(
        session.query(
            func.count(Transaction.id).label("transaction_count"),
        )
        .filter(Transaction.date.between(previous_start_date, previous_end_date))
        .first()[0]
        or 0
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
        session.query(
            func.count(Transaction.id).label("transaction_count"),
        )
        .filter(Transaction.date.between(current_start_date, current_end_date))
        .first()[0]
        or 0
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

    result_company_list = []
    for company in company_list:
        company = company._asdict()
        company["percentage"] = int(company["percentage"]) if company["percentage"] else 0
        company["difference_percentage"] = (
            int(company["difference_percentage"]) if company["difference_percentage"] else 0
        )
        result_company_list.append(company)

    result = {
        "success": True,
        "message": "OK",
        "result": {
            "company_list": result_company_list,
        },
    }

    assert response.status_code == 200
    assert response.json() == result


def test_get_current_month_insurance_company_rate_without_JWT():
    response = client.get("/api/dashboard/current-month-invoice-company-rate")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_current_month_insurance_company_rate_expired_JWT():
    token = expired_token

    response = client.get(
        "/api/dashboard/current-month-invoice-company-rate", headers={"Authorization": f"Bearer {token}"}
    )

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_current_month_insurance_company_rate_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get(
        "/api/dashboard/current-month-invoice-company-rate", headers={"Authorization": f"Bearer {token}"}
    )

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


conf_dict = asdict(conf())
db.init_app(app, **conf_dict)
Base.metadata.create_all(db.engine)
session = next(db.session())
create_test_users(session=session)
create_dummy_data(db)
expired_token = create_expired_jwt()
client = TestClient(app)
