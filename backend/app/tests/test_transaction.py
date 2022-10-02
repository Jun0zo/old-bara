from dataclasses import asdict
from uuid import uuid4

import bcrypt
from fastapi.testclient import TestClient

from app.common.config import conf
from app.database.conn import db, Base
from app.database.schema import Permission, InsuranceCompany, Transaction, User, UserRole
from app.main import app
from app.tests.create_expired_jwt import create_expired_jwt
from app.utils.jwt import auth_handler
from app.utils.date import get_now_datetime


def create_test_users(session):
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
        invoice="ARW",
    )

    User.create(
        session=session,
        auto_commit=True,
        email="driver@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김기사",
        role_id=UserRole.get(session=session, name="기사").id,
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
        invoice="SR",
    )

    User.create(
        session=session,
        auto_commit=True,
        email="manager@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김경리",
        role_id=UserRole.get(session=session, name="경리").id,
        status="accepted",
        plate_fee=0,
        contract_fee=0.0,
    )
    Permission.create(
        session=session,
        auto_commit=True,
        user_id=User.get(session=session, email="manager@baraman.net").id,
        user="AR",
        transaction="AR",
        invoice="AR",
    )

    User.create(
        session=session,
        auto_commit=True,
        email="registered@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김가입",
        status="registered",
    )

    User.create(
        session=session,
        auto_commit=True,
        email="verified@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김인증",
        status="verified",
    )

    User.create(
        session=session,
        auto_commit=True,
        email="deleted@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김탈퇴",
        status="deleted",
    )


def create_test_roles(session):
    UserRole.create(session=session, auto_commit=True, name="대표")
    UserRole.create(session=session, auto_commit=True, name="기사")
    UserRole.create(session=session, auto_commit=True, name="경리")


def create_test_JWT(user_id: str) -> str:
    return auth_handler.encode_token(subject=str(user_id))


def create_test_insurance_companys(session):
    InsuranceCompany.create(session=session, auto_commit=True, name="삼성화재")
    InsuranceCompany.create(session=session, auto_commit=True, name="애니카")
    InsuranceCompany.create(session=session, auto_commit=True, name="변경전")
    InsuranceCompany.create(session=session, auto_commit=True, name="삭제")


def create_test_transactions(session):
    user = User.get(session=session, email="admin@baraman.net")
    company = InsuranceCompany.get(session=session, name="삼성화재")
    Transaction.create(
        session=session,
        auto_commit=True,
        user_id=user.id,
        insurance_company_id=company.id,
        vehicle_id="00가 0000",
        vehicle_model="모닝",
        date=get_now_datetime().strftime("%Y-%m-%d"),
        price=300000,
        memo="test memo",
    )

    user = User.get(session=session, email="driver@baraman.net")
    company = InsuranceCompany.get(session=session, name="삼성화재")
    Transaction.create(
        session=session,
        auto_commit=True,
        user_id=user.id,
        insurance_company_id=company.id,
        vehicle_id="11가 1111",
        vehicle_model="모닝",
        date=get_now_datetime().strftime("%Y-%m-%d"),
        price=300000,
        memo="test memo",
    )


def test_create_transaction():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    test_date = get_now_datetime().strftime("%Y-%m-%d")

    response = client.post(
        "/api/transaction",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "12가 3456",
            "vehicle_model": "모닝",
            "date": test_date,
            "price": 300000,
            "memo": "test memo",
        },
    )

    session = next(db.session())
    response_json = response.json()
    created_object_id = response_json["result"]["created_object_id"]
    result = {"success": True, "message": "OK", "result": {"created_object_id": created_object_id}}

    assert response.status_code == 201
    assert response_json == result
    assert Transaction.get(session=session, id=created_object_id)


def test_create_transaction_invalid_params():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post(
        "/api/transaction",
        headers={"Authorization": f"Bearer {token}"},
        json={"뷁": "뷁"},
    )

    assert response.status_code == 422


def test_create_transaction_without_JWT():
    test_date = get_now_datetime().strftime("%Y-%m-%d")

    response = client.post(
        "/api/transaction",
        json={
            "insurance_company_id": 1,
            "vehicle_id": "12가 3456",
            "vehicle_model": "모닝",
            "date": test_date,
            "price": 300000,
            "memo": "test memo",
        },
    )

    response_json = response.json()
    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response_json == result


def test_create_transaction_expired_JWT():
    token = expired_token

    test_date = get_now_datetime().strftime("%Y-%m-%d")

    response = client.post(
        "/api/transaction",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "12가 3456",
            "vehicle_model": "모닝",
            "date": test_date,
            "price": 300000,
            "memo": "test memo",
        },
    )

    response_json = response.json()
    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response_json == result


def test_create_transaction_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    test_date = get_now_datetime().strftime("%Y-%m-%d")

    response = client.post(
        "/api/transaction",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "12가 3456",
            "vehicle_model": "모닝",
            "date": test_date,
            "price": 300000,
            "memo": "test memo",
        },
    )
    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_transaction_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    test_date = get_now_datetime().strftime("%Y-%m-%d")

    response = client.post(
        "/api/transaction",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "12가 3456",
            "vehicle_model": "모닝",
            "date": test_date,
            "price": 300000,
            "memo": "test memo",
        },
    )
    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_transaction_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    test_date = get_now_datetime().strftime("%Y-%m-%d")

    response = client.post(
        "/api/transaction",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "12가 3456",
            "vehicle_model": "모닝",
            "date": test_date,
            "price": 300000,
            "memo": "test memo",
        },
    )
    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_transaction_none_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="manager@baraman.net")
    token = create_test_JWT(test_user.id)

    test_date = get_now_datetime().strftime("%Y-%m-%d")

    response = client.post(
        "/api/transaction",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "12가 3456",
            "vehicle_model": "모닝",
            "date": test_date,
            "price": 300000,
            "memo": "test memo",
        },
    )

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_transaction_not_exists_company_id():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    test_date = get_now_datetime().strftime("%Y-%m-%d")

    response = client.post(
        "/api/transaction",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 99999,
            "vehicle_id": "12가 3456",
            "vehicle_model": "모닝",
            "date": test_date,
            "price": 300000,
            "memo": "test memo",
        },
    )

    result = {"success": False, "message": "존재하지 않는 보험사입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_get_transaction_with_AR_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction_user = User.get(session=session, email="driver@baraman.net")

    transaction = Transaction.filter(session=session, user_id=transaction_user.id).first()

    response = client.get(f"/api/transaction/{transaction.id}", headers={"Authorization": f"Bearer {token}"})

    session = next(db.session())
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
        .filter(Transaction.id == transaction.id)
        .first()
    )

    transaction = transaction._asdict()
    transaction["created_at"] = transaction["created_at"].strftime("%Y-%m-%dT%H:%M:%S")
    transaction["date"] = str(transaction["date"])

    result = {"success": True, "message": "OK", "result": transaction}

    assert response.status_code == 200
    assert response.json() == result


def test_get_transaction_with_own_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction = Transaction.filter(session=session, user_id=test_user.id).first()

    response = client.get(f"/api/transaction/{transaction.id}", headers={"Authorization": f"Bearer {token}"})

    session = next(db.session())
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
        .filter(Transaction.id == transaction.id)
        .first()
    )

    transaction = transaction._asdict()
    transaction["created_at"] = transaction["created_at"].strftime("%Y-%m-%dT%H:%M:%S")
    transaction["date"] = str(transaction["date"])

    result = {"success": True, "message": "OK", "result": transaction}

    assert response.status_code == 200
    assert response.json() == result


def test_get_transaction_without_JWT():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")

    transaction = Transaction.filter(session=session, user_id=test_user.id).first()

    response = client.get(f"/api/transaction/{transaction.id}")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_transaction_expired_JWT():
    token = expired_token

    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")

    transaction = Transaction.filter(session=session, user_id=test_user.id).first()

    response = client.get(f"/api/transaction/{transaction.id}", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_transaction_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/transaction/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_transaction_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/transaction/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_transaction_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/transaction/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_transaction_none_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction_user = User.get(session=session, email="admin@baraman.net")

    transaction = Transaction.get(session=session, user_id=transaction_user.id)

    response = client.get(f"/api/transaction/{transaction.id}", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_transaction_not_exists_transaction_id():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/transaction/99999", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "존재하지 않는 거래입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_transaction_other_transaction_with_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction_user = User.get(session=session, email="driver@baraman.net")

    transaction = Transaction.filter(session=session, user_id=transaction_user.id).first()

    response = client.put(
        f"/api/transaction/{transaction.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 2,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    session = next(db.session())
    result = {"success": True, "message": "OK", "result": {"updated_object_id": transaction.id}}

    assert response.status_code == 200
    assert response.json() == result
    assert Transaction.get(session=session, id=transaction.id).memo == "변경된 메모"


def test_update_transaction_with_own_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction = Transaction.filter(session=session, user_id=test_user.id).first()

    response = client.put(
        f"/api/transaction/{transaction.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모2",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    session = next(db.session())
    result = {"success": True, "message": "OK", "result": {"updated_object_id": transaction.id}}

    assert response.status_code == 200
    assert response.json() == result
    assert Transaction.get(session=session, id=transaction.id).memo == "변경된 메모2"


def test_update_transaction_without_params():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction = Transaction.filter(session=session, user_id=test_user.id).first()

    response = client.put(
        f"/api/transaction/{transaction.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"뷁": "뷁"}
    )

    result = {"success": False, "message": "수정할 값을 입력해 주세요!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_transaction_without_JWT():
    response = client.put(
        "/api/transaction/1",
        json={
            "insurance_company_id": 1,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모2",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_transaction_expired_JWT():
    token = expired_token

    response = client.put(
        "/api/transaction/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모2",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_update_transaction_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put(
        "/api/transaction/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모2",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_transaction_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put(
        "/api/transaction/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모2",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_transaction_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put(
        "/api/transaction/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모2",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_transaction_none_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction_user = User.get(session=session, email="admin@baraman.net")

    transaction = Transaction.filter(session=session, user_id=transaction_user.id).first()

    response = client.put(
        f"/api/transaction/{transaction.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모2",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_transaction_not_exists_transaction_id():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put(
        "/api/transaction/99999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 1,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모2",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    result = {"success": False, "message": "존재하지 않는 거래입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_transaction_not_exists_company_name():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction = Transaction.filter(session=session, user_id=test_user.id).first()

    response = client.put(
        f"/api/transaction/{transaction.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "insurance_company_id": 99999,
            "vehicle_id": "99가 9999",
            "vehicle_model": "모닝",
            "date": get_now_datetime().strftime("%Y-%m-%d"),
            "price": 300000,
            "memo": "변경된 메모2",
            "canceled": False,
            "cancel_fee": 0,
        },
    )

    result = {"success": False, "message": "존재하지 않는 보험사입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_delete_transaction_other_transaction_with_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction_user = User.get(session=session, email="driver@baraman.net")

    transaction = Transaction.filter(session=session, user_id=transaction_user.id).first()
    transaction_id = transaction.id

    response = client.delete(f"/api/transaction/{transaction_id}", headers={"Authorization": f"Bearer {token}"})

    session = next(db.session())
    result = {"success": True, "message": "OK", "result": {"deleted_object_id": transaction_id}}

    assert response.status_code == 200
    assert response.json() == result
    assert not Transaction.get(session=session, id=transaction_id)


def test_delete_transaction_with_own_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction = Transaction.filter(session=session, user_id=test_user.id).first()
    transaction_id = transaction.id

    response = client.delete(f"/api/transaction/{transaction_id}", headers={"Authorization": f"Bearer {token}"})

    session = next(db.session())
    result = {"success": True, "message": "OK", "result": {"deleted_object_id": transaction_id}}

    assert response.status_code == 200
    assert response.json() == result
    assert not Transaction.get(session=session, id=transaction_id)


def test_delete_transaction_without_JWT():
    response = client.delete("/api/transaction/1")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_transaction_expired_JWT():
    token = expired_token

    response = client.delete("/api/transaction/1", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_delete_transaction_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/transaction/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_transaction_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/transaction/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_transaction_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/transaction/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_transaction_none_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    transaction_user = User.get(session=session, email="admin@baraman.net")

    transaction = Transaction.filter(session=session, user_id=transaction_user.id).first()

    response = client.delete(f"/api/transaction/{transaction.id}", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_transaction_not_exists_transaction_id():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/transaction/99999", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "존재하지 않는 거래입니다!"}

    assert response.status_code == 400
    assert response.json() == result


conf_dict = asdict(conf())
db.init_app(app, **conf_dict)
Base.metadata.create_all(db.engine)
session = next(db.session())
create_test_roles(session=session)
create_test_users(session=session)
create_test_insurance_companys(session=session)
create_test_transactions(session=session)
expired_token = create_expired_jwt()
client = TestClient(app)
