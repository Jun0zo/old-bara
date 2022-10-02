from dataclasses import asdict
from uuid import uuid4

import bcrypt
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.common.config import conf
from app.database.conn import db, Base
from app.database.schema import InsuranceCompany, Permission, Transaction, User, UserRole
from app.main import app
from app.tests.create_expired_jwt import create_expired_jwt
from app.utils.jwt import auth_handler


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
        role_id=UserRole.get(session=session, name="기사").id,
        status="deleted",
        plate_fee=123,
        contract_fee=12.3,
    )
    Permission.create(
        session=session,
        auto_commit=True,
        user_id=User.get(session=session, email="deleted@baraman.net").id,
        user="SR",
        transaction="SRW",
        invoice="SR",
    )


def create_test_roles(session):
    UserRole.create(session=session, auto_commit=True, name="대표")
    UserRole.create(session=session, auto_commit=True, name="기사")
    UserRole.create(session=session, auto_commit=True, name="경리")


def create_test_insurancecompanies(session):
    InsuranceCompany.create(session=session, auto_commit=True, name="애니카")
    InsuranceCompany.create(session=session, auto_commit=True, name="삭제될회사")


def create_test_transaction(session):
    Transaction.create(
        session=session,
        auto_commit=True,
        user_id=1,
        insurance_company_id=1,
        vehicle_id="123가 1234",
        vehicle_model="벤츠 S500",
        date="2022-09-03",
        price=1234,
        memo="전역선물로벤츠주세요"
    )


def create_test_JWT(user_id: str) -> str:
    return auth_handler.encode_token(subject=str(user_id))


def test_create_insurancecompany():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "테스트"})

    session = next(db.session())
    response_json = response.json()
    created_object_id = response_json["result"]["created_object_id"]
    result = {"success": True, "message": "OK", "result": {"created_object_id": created_object_id}}

    assert response.status_code == 201
    assert response_json == result
    assert InsuranceCompany.get(session=session, id=created_object_id).name == "테스트"


def test_create_insurancecompany_invalid_params():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"뷁": "뷁"})

    result = {"detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_create_insurancecompany_without_JWT():
    response = client.post("/api/transaction/insurancecompany", json={"name": "테스트"})

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_insurancecompany_expired_JWT():
    token = expired_token

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "테스트"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_create_insurancecompany_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "테스트"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_insurancecompany_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "테스트"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_insurancecompany_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "테스트"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_insurancecompany_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "테스트"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_insurancecompany_short_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "뷁"})

    result = {"success": False, "message": "사명은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_insurancecompany_long_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "뷁"*99})

    result = {"success": False, "message": "사명은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_insurancecompany_blank_in_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "공 백 포 함"})

    result = {"success": False, "message": "사명에는 공백이 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_insurancecompany_special_chars_in_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/transaction/insurancecompany", headers={"Authorization": f"Bearer {token}"},
                           json={"name": "특!수@문#자$"})

    result = {"success": False, "message": "사명에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_insurancecompany_exists_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    test_insurancecompany = InsuranceCompany.get(session=session, id=1)

    response = client.post("/api/transaction/insurancecompany",
                           headers={"Authorization": f"Bearer {token}"}, json={"name": test_insurancecompany.name})

    result = {"success": False, "message": "이미 존재하는 회사입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_get_specific_insurancecompany():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    insurancecompany = InsuranceCompany.get(session=session, id=1,
                                            with_entities=[InsuranceCompany.id, InsuranceCompany.name])
    insurancecompany = jsonable_encoder(insurancecompany)
    result = {"success": True, "message": "OK", "result": insurancecompany}

    assert response.status_code == 200
    assert response.json() == result


def test_get_specific_insurancecompany_without_JWT():
    response = client.get("/api/transaction/insurancecompany/1")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_insurancecompany_expired_JWT():
    token = expired_token

    response = client.get("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_specific_insurancecompany_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_insurancecompany_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_insurancecompany_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_insurancecompany_not_exists_company():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/transaction/insurancecompany/9999999999", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "존재하지 않는 보험사입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_insurancecompany():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "변경됨"})

    session = next(db.session())
    response_json = response.json()
    updated_object_id = response_json["result"]["updated_object_id"]
    result = {"success": True, "message": "OK", "result": {"updated_object_id": updated_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert InsuranceCompany.get(session=session, id=updated_object_id).name == "변경됨"


def test_update_insurancecompany_invalid_params():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"뷁": "뷁"})

    result = {"detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_update_insurancecompany_without_JWT():
    response = client.put("/api/transaction/insurancecompany/1", json={"name": "변경됨"})

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_insurancecompany_expired_JWT():
    token = expired_token

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "변경됨"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_update_insurancecompany_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "변경됨"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_insurancecompany_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "변경됨"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_insurancecompany_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "변경됨"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_insurancecompany_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "변경됨"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_insurancecompany_short_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "뷁"})

    result = {"success": False, "message": "사명은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_insurancecompany_long_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "뷁"*99})

    result = {"success": False, "message": "사명은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_insurancecompany_blank_in_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "공 백 포 함"})

    result = {"success": False, "message": "사명에는 공백이 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_insurancecompany_special_chars_in_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"},
                          json={"name": "특!수@문#자$"})

    result = {"success": False, "message": "사명에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_insurancecompany_exists_insurancecompany_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    test_company = InsuranceCompany.get(session=session, id=1)

    response = client.put("/api/transaction/insurancecompany/1",
                          headers={"Authorization": f"Bearer {token}"}, json={"name": test_company.name})

    result = {"success": False, "message": "이미 존재하는 보험사입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_insurancecompany_not_exists_company():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/transaction/insurancecompany/9999999999",
                          headers={"Authorization": f"Bearer {token}"}, json={"name": "변경됨"})

    result = {"success": False, "message": "존재하지 않는 보험사입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_delete_insurancecompany():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    test_company_id = InsuranceCompany.get(session=session, name="삭제될회사").id

    response = client.delete(f"/api/transaction/insurancecompany/{test_company_id}",
                             headers={"Authorization": f"Bearer {token}"})

    session = next(db.session())
    response_json = response.json()
    deleted_object_id = response_json["result"]["deleted_object_id"]
    result = {"success": True, "message": "OK", "result": {"deleted_object_id": deleted_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert InsuranceCompany.get(session=session, id=deleted_object_id) is None


def test_delete_insurancecompany_without_JWT():
    response = client.delete("/api/transaction/insurancecompany/1")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_insurancecompany_expired_JWT():
    token = expired_token

    response = client.delete("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_delete_insurancecompany_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_insurancecompany_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_insurancecompany_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_insurancecompany_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/transaction/insurancecompany/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_insurancecompany_not_exists_company():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/transaction/insurancecompany/9999999999",
                             headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "존재하지 않는 보험사입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_delete_insurancecompany_using_company():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    test_company_id = Transaction.get(session=session, id=1).insurance_company_id

    response = client.delete(f"/api/transaction/insurancecompany/{test_company_id}",
                             headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "해당 보험사와 발생한 거래가 1건 이상 존재합니다!\n" +
                                           "데이터 무결성을 위해 거래가 존재하는 보험사는 삭제할 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


conf_dict = asdict(conf())
db.init_app(app, **conf_dict)
Base.metadata.create_all(db.engine)
session = next(db.session())
create_test_roles(session=session)
create_test_users(session=session)
create_test_insurancecompanies(session=session)
create_test_transaction(session=session)
expired_token = create_expired_jwt()
client = TestClient(app)
