from dataclasses import asdict
from operator import itemgetter
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
        email="driver2@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김기사2",
        role_id=UserRole.get(session=session, name="기사").id,
        status="accepted",
        plate_fee=5678,
        contract_fee=56.78,
    )
    Permission.create(
        session=session,
        auto_commit=True,
        user_id=User.get(session=session, email="driver2@baraman.net").id,
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
        email="registered2@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김가입2",
        status="registered",
    )

    User.create(
        session=session,
        auto_commit=True,
        email="registered3@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김가입3",
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
        email="verified2@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김인증2",
        status="verified",
    )

    User.create(
        session=session,
        auto_commit=True,
        email="verified3@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김인증3",
        status="verified",
    )

    User.create(
        session=session,
        auto_commit=True,
        email="verified4@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김인증4",
        status="verified",
    )

    User.create(
        session=session,
        auto_commit=True,
        email="verified5@baraman.net",
        email_token=uuid4().hex,
        password=bcrypt.hashpw("testpassword1!".encode("utf-8"), bcrypt.gensalt()),
        name="김인증5",
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


def create_test_JWT(user_id: str) -> str:
    return auth_handler.encode_token(subject=str(user_id))


def test_create_user():
    session = next(db.session())

    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "testpassword1!", "name": "김계정생성"})

    session = next(db.session())
    response_json = response.json()
    created_object_id = response_json["result"]["created_object_id"]
    result = {"success": True, "message": "OK", "result": {"created_object_id": created_object_id}}

    assert response.status_code == 201
    assert response_json == result
    assert User.get(session=session, id=created_object_id).email == "create_test@baraman.net"


def test_create_user_invalid_params():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "testpassword1!", "뷁": "뷁"})

    result = {"detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_create_user_invalid_email():
    response = client.post("/api/user",
                           json={"email": "뷁", "password": "testpassword1!", "name": "김계정생성"})

    result = {"detail": [{"loc": ["body", "email"],
                          "msg": "value is not a valid email address",
                          "type": "value_error.email"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_create_user_short_password():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "a", "name": "김계정생성"})

    result = {"success": False, "message": "비밀번호는 8자 이상, 20자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_long_password():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "a"*99, "name": "김계정생성"})

    result = {"success": False, "message": "비밀번호는 8자 이상, 20자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_password_without_number():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "testpassword!", "name": "김계정생성"})

    result = {"success": False, "message": "비밀번호는 최소 1개 이상의 숫자가 포함되어 있어야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_password_without_alphabet():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "1234567!", "name": "김계정생성"})

    result = {"success": False, "message": "비밀번호는 최소 1개 이상의 영문 대문자 또는 소문자가 포함되어 있어야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_password_without_special_chars():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "testpassword1", "name": "김계정생성"})

    result = {"success": False, "message": "비밀번호는 최소 1개 이상의 특수문자(~!@#$%^&*.?)가 포함되어 있어야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_short_name():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "testpassword1!", "name": "뷁"})

    result = {"success": False, "message": "이름은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_long_name():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "testpassword1!", "name": "뷁"*99})

    result = {"success": False, "message": "이름은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_blank_in_name():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "testpassword1!", "name": "공 백 포 함"})

    result = {"success": False, "message": "이름에는 공백이 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_special_chars_in_name():
    response = client.post("/api/user",
                           json={"email": "create_test@baraman.net", "password": "testpassword1!", "name": "특!수@문#자$"})

    result = {"success": False, "message": "이름에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_exists_and_not_registered_status_email():
    response = client.post("/api/user",
                           json={"email": "admin@baraman.net", "password": "testpassword1!", "name": "김계정생성"})

    result = {"success": False, "message": "이미 존재하는 이메일입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_create_user_exists_and_registered_status_email():
    response = client.post("/api/user",
                           json={"email": "registered2@baraman.net", "password": "testpassword1!", "name": "김가입2"})

    session = next(db.session())
    response_json = response.json()
    created_object_id = response_json["result"]["created_object_id"]
    result = {"success": True, "message": "OK", "result": {"created_object_id": created_object_id}}

    assert response.status_code == 201
    assert response_json == result
    assert User.get(session=session, id=created_object_id).email == "registered2@baraman.net"


def test_get_all_user():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user", headers={"Authorization": f"Bearer {token}"})

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
    users = jsonable_encoder(users)
    result = {"success": True, "message": "OK", "result": users}

    assert response.status_code == 200
    assert response.json() == result


def test_get_all_user_without_JWT():
    response = client.get("/api/user")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_all_user_expired_JWT():
    token = expired_token

    response = client.get("/api/user", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_all_user_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_all_user_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_all_user_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_all_user_with_none_AR_or_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_user_verified():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified@baraman.net").id

    response = client.get(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"})

    user = User.filter(
        session=session,
        id=target_user_id,
        status="verified",
        with_entities=[User.id, User.email, User.name, User.status],
    ).first()
    user = jsonable_encoder(user)
    result = {"success": True, "message": "OK", "result": user}

    assert response.status_code == 200
    assert response.json() == result


def test_get_specific_user_accepted():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="driver@baraman.net").id

    response = client.get(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"})

    user = (
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
    user = jsonable_encoder(user)
    result = {"success": True, "message": "OK", "result": user}

    assert response.status_code == 200
    assert response.json() == result


def test_get_specific_user_deleted():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="deleted@baraman.net").id

    response = client.get(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"})

    user = (
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
    user = jsonable_encoder(user)
    result = {"success": True, "message": "OK", "result": user}

    assert response.status_code == 200
    assert response.json() == result


def test_get_specific_user_without_JWT():
    response = client.get("/api/user/1")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_user_expired_JWT():
    token = expired_token

    response = client.get("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_get_specific_user_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_user_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_user_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_user_with_none_AR_or_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_get_specific_user_with_none_AR_or_ARW_permission_but_target_self():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = test_user.id

    response = client.get(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"})

    user = (
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
    user = jsonable_encoder(user)
    result = {"success": True, "message": "OK", "result": user}

    assert response.status_code == 200
    assert response.json() == result


def test_get_specific_user_not_exists_user():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.get("/api/user/99", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "존재하지 않거나 탈퇴된 계정입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_self_registered():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = test_user.id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={"current_password": "testpassword1!",
                                "new_password": "testpassword2!", "new_password_check": "testpassword2!"})

    result = {"success": False, "message": "존재하지 않거나 탈퇴된 계정입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_self_verified():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = test_user.id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={"current_password": "testpassword1!",
                                "new_password": "testpassword2!", "new_password_check": "testpassword2!"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_user_self_deleted():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = test_user.id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={"current_password": "testpassword1!",
                                "new_password": "testpassword2!", "new_password_check": "testpassword2!"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_user_self_accpted():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = test_user.id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={"current_password": "testpassword1!",
                                "new_password": "testpassword2!", "new_password_check": "testpassword2!"})

    session = next(db.session())
    response_json = response.json()
    updated_object_id = response_json["result"]["updated_object_id"]
    result = {"success": True, "message": "OK", "result": {"updated_object_id": updated_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert User.get(session=session, id=updated_object_id).email == "admin@baraman.net"


def test_update_user_self_accpted_invalid_params():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = test_user.id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={"뷁": "뷁",
                                "new_password": "testpassword2!", "new_password_check": "testpassword2!"})

    result = {"success": False, "message": "모든 값을 입력해 주세요!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_self_accpted_passwords_do_not_match():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = test_user.id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={"current_password": "testpassword1!",
                                "new_password": "testpassword2!", "new_password_check": "뷁"})

    result = {"success": False, "message": "비밀번호와 비밀번호 확인값이 일치하지 않습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_self_accpted_wrong_password():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = test_user.id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={"current_password": "뷁",
                                "new_password": "testpassword2!", "new_password_check": "testpassword2!"})

    result = {"success": False, "message": "비밀번호가 틀립니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_without_JWT():
    response = client.put("/api/user/1")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_update_user_expired_JWT():
    token = expired_token

    response = client.put("/api/user/1", headers={"Authorization": f"Bearer {token}"},
                          json={"current_password": "testpassword1!",
                                "new_password": "testpassword2!", "new_password_check": "testpassword2!"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_update_user_init_only():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified2@baraman.net").id
    role_id = UserRole.get(session=session, name="기사").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={
                              "role_id": role_id,
                              "status": "accepted",
                              "permission_user": "SR",
                              "permission_transaction": "SRW",
                              "permission_invoice": "SR"
                          })

    session = next(db.session())
    response_json = response.json()
    updated_object_id = response_json["result"]["updated_object_id"]
    updated_object = User.get(session=session, id=updated_object_id)
    updated_object_permission = Permission.get(session=session, user_id=updated_object.id)
    result = {"success": True, "message": "OK", "result": {"updated_object_id": updated_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert updated_object.email == "verified2@baraman.net"
    assert updated_object.role_id == role_id
    assert updated_object.status == "accepted"
    assert updated_object_permission.user == "SR"
    assert updated_object_permission.transaction == "SRW"
    assert updated_object_permission.invoice == "SR"


def test_update_user_init_only_with_wrong_role_id():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified3@baraman.net").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={
                              "role_id": 99,
                              "status": "accepted",
                              "permission_user": "SR",
                              "permission_transaction": "SRW",
                              "permission_invoice": "SR"
                          })

    result = {"success": False, "message": "변경 대상 역할이 존재하지 않습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_init_only_without_role_id():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified3@baraman.net").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={
                              "status": "accepted",
                              "permission_user": "SR",
                              "permission_transaction": "SRW",
                              "permission_invoice": "SR"
                          })

    result = {"success": False, "message": "역할은 반드시 지정해야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_init_only_without_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified3@baraman.net").id
    role_id = UserRole.get(session=session, name="기사").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={"role_id": role_id})

    result = {"success": False, "message": "현재 사용자의 권한이 지정되어 있지 않습니다. 권한을 지정해 주세요!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified3@baraman.net").id
    role_id = UserRole.get(session=session, name="기사").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={
                              "name": "김변경완료",
                              "role_id": role_id,
                              "status": "accepted",
                              "plate_fee": 1000,
                              "contract_fee": 10.0,
                              "permission_user": "SR",
                              "permission_transaction": "SRW",
                              "permission_invoice": "SR"
                          })

    session = next(db.session())
    response_json = response.json()
    updated_object_id = response_json["result"]["updated_object_id"]
    updated_object = User.get(session=session, id=updated_object_id)
    updated_object_permission = Permission.get(session=session, user_id=updated_object.id)
    result = {"success": True, "message": "OK", "result": {"updated_object_id": updated_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert updated_object.email == "verified3@baraman.net"
    assert updated_object.name == "김변경완료"
    assert updated_object.role_id == role_id
    assert updated_object.status == "accepted"
    assert updated_object.plate_fee == 1000
    assert updated_object.contract_fee == 10.0
    assert updated_object_permission.user == "SR"
    assert updated_object_permission.transaction == "SRW"
    assert updated_object_permission.invoice == "SR"


def test_update_user_short_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified4@baraman.net").id
    role_id = UserRole.get(session=session, name="기사").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={
                              "name": "뷁",
                              "role_id": role_id,
                              "status": "accepted",
                              "plate_fee": 1000,
                              "contract_fee": 10.0,
                              "permission_user": "SR",
                              "permission_transaction": "SRW",
                              "permission_invoice": "SR"
                          })

    session = next(db.session())
    result = {"success": False, "message": "이름은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_long_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified4@baraman.net").id
    role_id = UserRole.get(session=session, name="기사").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={
                              "name": "뷁"*99,
                              "role_id": role_id,
                              "status": "accepted",
                              "plate_fee": 1000,
                              "contract_fee": 10.0,
                              "permission_user": "SR",
                              "permission_transaction": "SRW",
                              "permission_invoice": "SR"
                          })

    session = next(db.session())
    result = {"success": False, "message": "이름은 2자 이상, 10자 이하여야 합니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_blank_in_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified4@baraman.net").id
    role_id = UserRole.get(session=session, name="기사").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={
                              "name": "공 백 포 함",
                              "role_id": role_id,
                              "status": "accepted",
                              "plate_fee": 1000,
                              "contract_fee": 10.0,
                              "permission_user": "SR",
                              "permission_transaction": "SRW",
                              "permission_invoice": "SR"
                          })

    session = next(db.session())
    result = {"success": False, "message": "이름에는 공백이 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_special_chars_in_name():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified4@baraman.net").id
    role_id = UserRole.get(session=session, name="기사").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={
                              "name": "특!수@문#자$",
                              "role_id": role_id,
                              "status": "accepted",
                              "plate_fee": 1000,
                              "contract_fee": 10.0,
                              "permission_user": "SR",
                              "permission_transaction": "SRW",
                              "permission_invoice": "SR"
                          })

    session = next(db.session())
    result = {"success": False, "message": "이름에는 특수문자(~!@#$%^&*.?)가 포함될 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_update_user_invalid_params():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified4@baraman.net").id
    role_id = UserRole.get(session=session, name="기사").id

    response = client.put(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"},
                          json={
                              "name": "김변경완료",
                              "role_id": role_id,
                              "status": "accepted",
                              "plate_fee": "뷁",
                              "contract_fee": 10.0,
                              "permission_user": "SR",
                              "permission_transaction": "SRW",
                              "permission_invoice": "SR"
                          })

    session = next(db.session())
    result = {"detail": [{"loc": ["body", "plate_fee"],
                          "msg": "value is not a valid integer",
                          "type": "type_error.integer"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_delete_user_accepted_status_user():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="driver2@baraman.net").id

    response = client.delete(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"})

    session = next(db.session())
    response_json = response.json()
    withdrawn_object_id = response_json["result"]["withdrawn_object_id"]
    result = {"success": True, "message": "OK", "result": {"withdrawn_object_id": withdrawn_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert User.get(session=session, id=withdrawn_object_id).status == "deleted"


def test_delete_user_registered_status_user():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="registered3@baraman.net").id

    response = client.delete(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"})

    session = next(db.session())
    response_json = response.json()
    deleted_object_id = response_json["result"]["deleted_object_id"]
    result = {"success": True, "message": "OK", "result": {"deleted_object_id": deleted_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert User.get(session=session, id=deleted_object_id) is None


def test_delete_user_verified_status_user():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="verified5@baraman.net").id

    response = client.delete(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"})

    session = next(db.session())
    response_json = response.json()
    deleted_object_id = response_json["result"]["deleted_object_id"]
    result = {"success": True, "message": "OK", "result": {"deleted_object_id": deleted_object_id}}

    assert response.status_code == 200
    assert response_json == result
    assert User.get(session=session, id=deleted_object_id) is None


def test_delete_user_deleted_status_user():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)
    target_user_id = User.get(session=session, email="deleted@baraman.net").id

    response = client.delete(f"/api/user/{target_user_id}", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "이미 탈퇴된 계정입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_delete_user_without_JWT():
    response = client.delete("/api/user/1")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_user_expired_JWT():
    token = expired_token

    response = client.delete("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_delete_user_with_registered_status():
    session = next(db.session())
    test_user = User.get(session=session, email="registered@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_user_with_verified_status():
    session = next(db.session())
    test_user = User.get(session=session, email="verified@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_user_with_deleted_status():
    session = next(db.session())
    test_user = User.get(session=session, email="deleted@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_user_with_none_AR_or_ARW_permission():
    session = next(db.session())
    test_user = User.get(session=session, email="driver@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "권한이 없습니다!"}

    assert response.status_code == 403
    assert response.json() == result


def test_delete_user_taget_self():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/1", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "본인 계정은 삭제할 수 없습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_delete_user_not_exists_user():
    session = next(db.session())
    test_user = User.get(session=session, email="admin@baraman.net")
    token = create_test_JWT(test_user.id)

    response = client.delete("/api/user/99", headers={"Authorization": f"Bearer {token}"})

    result = {"success": False, "message": "존재하지 않거나 탈퇴된 계정입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_login():
    response = client.post("/api/user/login", json={"email": "manager@baraman.net", "password": "testpassword1!"})
    response_json = response.json()
    user_id = User.get(session=session, email="manager@baraman.net").id
    user_id_from_access_token = int(auth_handler.decode_token(token=response_json["access_token"]))
    new_access_token = auth_handler.refresh_token(response_json["refresh_token"])
    user_id_from_new_access_token = int(auth_handler.decode_token(token=new_access_token))

    assert response.status_code == 200
    assert response_json["success"] is True
    assert response_json["message"] == "OK"
    assert user_id == user_id_from_access_token == user_id_from_new_access_token


def test_login_with_invalid_params():
    response = client.post("/api/user/login", json={"뷁": "뷁", "password": "testpassword1!"})

    result = {"detail": [{"loc": ["body", "email"],
                          "msg": "field required",
                          "type": "value_error.missing"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_login_not_exists_email():
    response = client.post("/api/user/login", json={"email": "asdf@baraman.net", "password": "testpassword1!"})

    result = {"success": False, "message": "존재하지 않거나 탈퇴된 계정입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_login_wrong_password():
    response = client.post("/api/user/login", json={"email": "manager@baraman.net", "password": "뷁"})

    result = {"success": False, "message": "비밀번호가 틀립니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_login_registered_status_user():
    response = client.post("/api/user/login", json={"email": "registered@baraman.net", "password": "testpassword1!"})

    result = {"success": False, "message": "이메일 인증을 완료해 주세요!\n인증 메일이 도착하지 않았다면 스팸 메일함을 확인해 주세요!"}

    assert response.status_code == 400
    assert response.json() == result


def test_login_verified_status_user():
    response = client.post("/api/user/login", json={"email": "verified@baraman.net", "password": "testpassword1!"})

    result = {"success": False, "message": "관리자 승인 대기 중인 계정입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_login_deleted_status_user():
    response = client.post("/api/user/login", json={"email": "deleted@baraman.net", "password": "testpassword1!"})

    result = {"success": False, "message": "존재하지 않거나 탈퇴된 계정입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_refresh():
    session = next(db.session())
    target_user_id = User.get(session=session, email="manager@baraman.net").id
    refresh_token = auth_handler.encode_refresh_token(subject=str(target_user_id))

    response = client.get("/api/user/token/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
    response_json = response.json()

    new_access_token = response_json["access_token"]
    user_id_from_new_access_token = int(auth_handler.decode_token(token=new_access_token))

    assert response.status_code == 200
    assert response_json["success"] is True
    assert response_json["message"] == "OK"
    assert target_user_id == user_id_from_new_access_token


def test_refresh_without_JWT():
    response = client.get("/api/user/token/refresh")

    result = {"detail": "Not authenticated"}

    assert response.status_code == 403
    assert response.json() == result


def test_refresh_expired_JWT():
    token = expired_token

    response = client.get("/api/user/token/refresh", headers={"Authorization": f"Bearer {token}"})

    result = {"detail": "Refresh token expired"}

    assert response.status_code == 401
    assert response.json() == result


def test_verify_email():
    session = next(db.session())
    target_user = User.get(session=session, email="registered@baraman.net")

    client.get(f"/api/user/verify-email/{target_user.email_token}")

    session = next(db.session())
    target_user = User.get(session=session, email="registered@baraman.net")

    assert target_user.status == "verified"


def test_verify_email_not_exists_token():
    response = client.get("/api/user/verify-email/asdf")

    result = "<html><script>alert('인증 토큰이 유효하지 않습니다!');location.href='/';</script></html>"

    assert response.status_code == 400
    assert response.text == result


def test_send_password_reset_mail():
    session = next(db.session())
    target_user = User.get(session=session, email="manager@baraman.net")
    previous_email_token = target_user.email_token

    response = client.get(f"/api/user/reset-password/{target_user.email}")

    session = next(db.session())
    current_email_token = User.get(session=session, email="manager@baraman.net").email_token
    result = {"success": True, "message": "OK"}

    assert response.status_code == 200
    assert response.json() == result
    assert previous_email_token != current_email_token


def test_send_password_reset_mail_invalid_email():
    response = client.get("/api/user/reset-password/뷁")

    result = {"detail": [{"loc": ["path", "target_user_mail"],
                          "msg": "value is not a valid email address",
                          "type": "value_error.email"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_send_password_reset_mail_registered_status_user():
    response = client.get("/api/user/reset-password/registered2@baraman.net")

    result = {"success": False, "message": "존재하지 않거나 탈퇴된 계정입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_send_password_reset_mail_deleted_status_user():
    response = client.get("/api/user/reset-password/deleted@baraman.net")

    result = {"success": False, "message": "존재하지 않거나 탈퇴된 계정입니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_reset_password():
    session = next(db.session())
    target_user = User.get(session=session, email="driver@baraman.net")

    response = client.post("/api/user/reset-password",
                           json={"token": target_user.email_token,
                                 "new_password": "testpassword2!",
                                 "new_password_check": "testpassword2!"})

    session = next(db.session())
    response_json = response.json()
    updated_object_id = response_json["result"]["updated_object_id"]
    updated_object = User.get(session=session, id=updated_object_id)
    result = {"success": True, "message": "OK", "result": {"updated_object_id": updated_object_id}}

    assert response.status_code == 200
    assert response.json() == result
    assert bcrypt.checkpw("testpassword2!".encode("utf-8"), updated_object.password.encode("utf-8")) is True


def test_reset_password_invalid_params():
    response = client.post("/api/user/reset-password",
                           json={"뷁": "뷁",
                                 "new_password": "testpassword2!",
                                 "new_password_check": "testpassword2!"})

    result = {"detail": [{"loc": ["body", "token"], "msg": "field required", "type": "value_error.missing"}]}

    assert response.status_code == 422
    assert response.json() == result


def test_reset_password_invalid_token():
    response = client.post("/api/user/reset-password",
                           json={"token": "뷁",
                                 "new_password": "testpassword2!",
                                 "new_password_check": "testpassword2!"})

    result = {"success": False, "message": "인증 토큰이 유효하지 않습니다!"}

    assert response.status_code == 400
    assert response.json() == result


def test_reset_passwords_do_not_match():
    session = next(db.session())
    target_user = User.get(session=session, email="driver@baraman.net")

    response = client.post("/api/user/reset-password",
                           json={"token": target_user.email_token,
                                 "new_password": "testpassword2!",
                                 "new_password_check": "뷁"})

    result = {"success": False, "message": "비밀번호와 비밀번호 확인값이 일치하지 않습니다!"}

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
