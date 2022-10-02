from dataclasses import asdict
from uuid import uuid4

import bcrypt
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.common.config import conf
from app.database.conn import db, Base
from app.database.schema import Permission, User, UserRole
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
    UserRole.create(session=session, auto_commit=True, name="아무도지정안된역할")


def create_test_JWT(user_id: str) -> str:
    return auth_handler.encode_token(subject=str(user_id))


def test_create_role():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "테스트"})

    session = next(db.session())
    response_json = response.json()
    created_object_id = response_json["result"]["created_object_id"]
    result = {"success": True, "message": "OK", "result": {"created_object_id": created_object_id}}

    assert response.status_code == 201
    assert response_json == result
    assert UserRole.get(session=session, id=created_object_id).name == "테스트"


def test_create_role_invalid_params():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"뷁": "뷁"})

    result = {"detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_create_role_without_JWT():
    response = client.post("/api/user/role", json={"name": "테스트"})

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_role_expired_JWT():
    token = expired_token

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "테스트"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_create_role_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "테스트"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_role_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "테스트"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_role_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "테스트"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_role_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "테스트"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_create_role_short_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "뷁"})

    result = {"success": False, "message": "역할 이름은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_role_long_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "뷁"*99})

    result = {"success": False, "message": "역할 이름은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_role_blank_in_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "공 백 포 함"})

    result = {"success": False, "message": "역할 이름에는 공백이 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_role_special_chars_in_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.post("/api/user/role", headers={"Authorization": f"Bearer {token}"}, json={"name": "특!수@문#자$"})

    result = {"success": False, "message": "역할 이름에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_role_exists_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    test_role = UserRole.get(session=session, id=1)

    response = client.post("/api/user/role",
                           headers={"Authorization": f"Bearer {token}"}, json={"name": test_role.name})

    result = {"success": False, "message": "이미 존재하는 역할입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_get_all_role():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/role", headers={"Authorization": f"Bearer {token}"})

    roles = UserRole.filter(session=session, with_entities=[UserRole.id, UserRole.name]).order_by("id").all()
    roles = jsonable_encoder(roles)
    result = {"success": True, "message": "OK", "result": roles}

    assert response.status_code == 200
    assert response.json() == result


def test_get_all_role_without_JWT():
    response = client.get("/api/user/role")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_all_role_expired_JWT():
    token = expired_token

    response = client.get("/api/user/role", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_all_role_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/role", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_all_role_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/role", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_all_role_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/role", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_role():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    role = UserRole.get(session=session, id=1, with_entities=[UserRole.id, UserRole.name])
    role = jsonable_encoder(role)
    result = {"success": True, "message": "OK", "result": role}

    assert response.status_code == 200
    assert response.json() == result


def test_get_specific_role_without_JWT():
    response = client.get("/api/user/role/1")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_role_expired_JWT():
    token = expired_token

    response = client.get("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_specific_role_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_role_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_role_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_role_not_exists_role():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/role/9999999999", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "존재하지 않는 역할입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_role():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "변경됨"})

    session = next(db.session())
    response_json = response.json()
    updated_object_id = response_json["result"]["updated_object_id"]
    result = {"success": True, "message": "OK", "result": {"updated_object_id": updated_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert UserRole.get(session=session, id=updated_object_id).name == "변경됨"


def test_update_role_invalid_params():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"뷁": "뷁"})

    result = {"detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_update_role_without_JWT():
    response = client.put("/api/user/role/1", json={"name": "변경됨"})

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_role_expired_JWT():
    token = expired_token

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "변경됨"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_update_role_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "변경됨"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_role_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "변경됨"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_role_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "변경됨"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_role_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "변경됨"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_role_short_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "뷁"})

    result = {"success": False, "message": "역할 이름은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_role_long_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "뷁"*99})

    result = {"success": False, "message": "역할 이름은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_role_blank_in_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "공 백 포 함"})

    result = {"success": False, "message": "역할 이름에는 공백이 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_role_special_chars_in_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/1", headers={"Authorization": f"Bearer {token}"}, json={"name": "특!수@문#자$"})

    result = {"success": False, "message": "역할 이름에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_role_exists_role_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    test_role = UserRole.get(session=session, id=1)

    response = client.put("/api/user/role/1",
                          headers={"Authorization": f"Bearer {token}"}, json={"name": test_role.name})

    result = {"success": False, "message": "이미 존재하는 역할 이름입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_role_not_exists_role():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.put("/api/user/role/9999999999",
                          headers={"Authorization": f"Bearer {token}"}, json={"name": "변경됨"})

    result = {"success": False, "message": "존재하지 않는 역할입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_delete_role():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    test_role_id = UserRole.get(session=session, name="아무도지정안된역할").id

    response = client.delete(f"/api/user/role/{test_role_id}", headers={"Authorization": f"Bearer {token}"})

    session = next(db.session())
    response_json = response.json()
    deleted_object_id = response_json["result"]["deleted_object_id"]
    result = {"success": True, "message": "OK", "result": {"deleted_object_id": deleted_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert UserRole.get(session=session, id=deleted_object_id) is None


def test_delete_role_without_JWT():
    response = client.delete("/api/user/role/1")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_role_expired_JWT():
    token = expired_token

    response = client.delete("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_delete_role_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_role_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_role_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_role_with_none_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/role/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_role_not_exists_role():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/role/9999999999", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "존재하지 않는 역할입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_delete_role_using_role():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    test_role_id = test_user.role_id

    response = client.delete(f"/api/user/role/{test_role_id}", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "해당 역할로 지정된 사용자가 1명 이상 존재합니다!\n" +
                                           "사용자의 역할을 다른 역할로 변경한 후에 다시 시도해 주세요!"}

    assert response.status_code == 400
    assert response.json() == result


conf_dict = asdict(conf())
db.init_app(app, **conf_dict)
Base.metadata.create_all(db.engine)
session = next(db.session())
create_test_roles(session=session)
create_test_users(session=session)
expired_token = create_expired_jwt()
client = TestClient(app)
