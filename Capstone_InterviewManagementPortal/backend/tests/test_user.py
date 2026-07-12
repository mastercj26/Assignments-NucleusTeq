import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Database
from src.core.security import hash_password
from src.enums.user_enums import UserRole, UserStatus

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    db = Database.connect()
    db["users"].delete_many({})
    yield
    db["users"].delete_many({})


def get_admin_token():
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "admin@nucleusteq.com",
            "password": hash_password("admin123"),
            "role": UserRole.ADMIN,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
            "first_name": "Admin",
            "last_name": "User",
        }
    )
    res = client.post("/auth/login", json={"email": "admin@nucleusteq.com", "password": "admin123"})
    return res.json()["access_token"]


def get_hr_token():
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "hr@nucleusteq.com",
            "password": hash_password("hrpass123"),
            "role": UserRole.HR,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
            "first_name": "HR",
            "last_name": "User",
        }
    )
    res = client.post("/auth/login", json={"email": "hr@nucleusteq.com", "password": "hrpass123"})
    return res.json()["access_token"]


def test_create_user_success():
    token = get_admin_token()
    res = client.post(
        "/users/",
        json={
            "email": "newhr@nucleusteq.com",
            "password": "Secure@1",
            "first_name": "New",
            "last_name": "HR",
            "role": "hr",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "newhr@nucleusteq.com"
    assert data["role"] == "hr"
    assert data["is_first_login"] is True
    assert data["status"] == "first_login"


def test_create_user_duplicate_email():
    token = get_admin_token()
    payload = {
        "email": "dup@nucleusteq.com",
        "password": "Secure@1",
        "first_name": "Dup",
        "last_name": "User",
        "role": "hr",
    }
    client.post("/users/", json=payload, headers={"Authorization": f"Bearer {token}"})
    res = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 409


def test_create_user_non_admin_forbidden():
    get_admin_token()
    hr_token = get_hr_token()
    res = client.post(
        "/users/",
        json={
            "email": "new@nucleusteq.com",
            "password": "Secure@1",
            "first_name": "New",
            "last_name": "User",
            "role": "interviewer",
        },
        headers={"Authorization": f"Bearer {hr_token}"},
    )
    assert res.status_code == 403


def test_list_users():
    token = get_admin_token()
    for i in range(3):
        client.post(
            "/users/",
            json={
                "email": f"user{i}@nucleusteq.com",
                "password": "Secure@1",
                "first_name": ["Alpha", "Beta", "Gamma", "Delta", "Echo"][i],
                "last_name": "Test",
                "role": "interviewer",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

    res = client.get("/users/?page=1&per_page=2", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 4
    assert len(data["users"]) == 2


def test_get_user_by_id():
    token = get_admin_token()
    create_res = client.post(
        "/users/",
        json={
            "email": "findme@nucleusteq.com",
            "password": "Secure@1",
            "first_name": "Find",
            "last_name": "Me",
            "role": "hr",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    user_id = create_res.json()["id"]

    res = client.get(f"/users/{user_id}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "findme@nucleusteq.com"


def test_update_user():
    token = get_admin_token()
    create_res = client.post(
        "/users/",
        json={
            "email": "update@nucleusteq.com",
            "password": "Secure@1",
            "first_name": "Old",
            "last_name": "Name",
            "role": "hr",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    user_id = create_res.json()["id"]

    res = client.put(
        f"/users/{user_id}",
        json={
            "first_name": "New",
            "last_name": "Name",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json()["first_name"] == "New"


def test_disable_user():
    token = get_admin_token()
    create_res = client.post(
        "/users/",
        json={
            "email": "disable@nucleusteq.com",
            "password": "Secure@1",
            "first_name": "Dis",
            "last_name": "Able",
            "role": "hr",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    user_id = create_res.json()["id"]

    res = client.patch(
        f"/users/{user_id}/disable?active=false", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json()["user"]["status"] == "inactive"

    res = client.patch(
        f"/users/{user_id}/disable?active=true", headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200
    assert res.json()["user"]["status"] == "active"


def test_create_user_without_password_uses_default():
    """User created without password gets the default one."""
    token = get_admin_token()
    res = client.post(
        "/users/",
        json={
            "email": "defaultpw@nucleusteq.com",
            "first_name": "Default",
            "last_name": "Password",
            "role": "interviewer",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    assert res.json()["is_first_login"] is True

    # Login with the default password is blocked until the password is reset
    res = client.post(
        "/auth/login", json={"email": "defaultpw@nucleusteq.com", "password": "admin123"}
    )
    assert res.status_code == 401
    assert "reset your password" in res.json()["message"].lower()

    # Reset with the default as the old password, then login works
    res = client.post(
        "/auth/reset-password",
        json={
            "email": "defaultpw@nucleusteq.com",
            "old_password": "admin123",
            "new_password": "newpass1!",
        },
    )
    assert res.status_code == 200

    res = client.post(
        "/auth/login", json={"email": "defaultpw@nucleusteq.com", "password": "newpass1!"}
    )
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_create_user_persists_to_db():
    """Created user should exist in DB with hashed password."""
    token = get_admin_token()
    res = client.post(
        "/users/",
        json={
            "email": "dbcheck@nucleusteq.com",
            "first_name": "Db",
            "last_name": "Check",
            "role": "hr",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201

    db = Database.connect()
    doc = db["users"].find_one({"email": "dbcheck@nucleusteq.com"})
    assert doc is not None
    assert doc["is_first_login"] is True
    assert doc["password"] != "admin123"  # never stored in plaintext
    assert "password" not in res.json()  # never returned in responses


def test_update_user_persists_to_db():
    token = get_admin_token()
    res = client.post(
        "/users/",
        json={
            "email": "updater@nucleusteq.com",
            "first_name": "Before",
            "last_name": "Update",
            "role": "hr",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    user_id = res.json()["id"]

    res = client.put(
        f"/users/{user_id}",
        json={"first_name": "After"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200

    from bson import ObjectId

    db = Database.connect()
    doc = db["users"].find_one({"_id": ObjectId(user_id)})
    assert doc["first_name"] == "After"


def test_create_user_rejects_special_chars():
    """Names with digits/symbols and emails with special chars should fail."""
    token = get_admin_token()
    auth = {"Authorization": f"Bearer {token}"}
    base = {"email": "valid@nucleusteq.com", "first_name": "Ravi", "last_name": "Sharma", "role": "hr"}

    res = client.post("/users/", json={**base, "first_name": "Ravi123"}, headers=auth)
    assert res.status_code == 422

    res = client.post("/users/", json={**base, "last_name": "Sharma@"}, headers=auth)
    assert res.status_code == 422

    res = client.post("/users/", json={**base, "email": "ra#vi@nucleusteq.com"}, headers=auth)
    assert res.status_code == 422

    # normal name with space should work
    res = client.post("/users/", json={**base, "first_name": "Ravi Kumar"}, headers=auth)
    assert res.status_code == 201


def test_hr_can_list_interviewers():
    """HR needs interviewer options for scheduling, without full user access."""
    db = Database.connect()
    db["users"].insert_many([
        {"email": "hr@nucleusteq.com", "password": hash_password("hrpass12"),
         "role": UserRole.HR, "status": UserStatus.ACTIVE, "is_first_login": False},
        {"email": "iva@nucleusteq.com", "password": hash_password("ivpass12"),
         "role": UserRole.INTERVIEWER, "status": UserStatus.ACTIVE, "is_first_login": False,
         "first_name": "Iva", "last_name": "Active"},
        {"email": "ivb@nucleusteq.com", "password": hash_password("ivpass12"),
         "role": UserRole.INTERVIEWER, "status": UserStatus.INACTIVE, "is_first_login": False,
         "first_name": "Ivb", "last_name": "Disabled"},
    ])
    token = client.post("/auth/login", json={
        "email": "hr@nucleusteq.com", "password": "hrpass12"
    }).json()["access_token"]

    res = client.get("/users/interviewers", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    emails = [u["email"] for u in res.json()]
    assert "iva@nucleusteq.com" in emails
    assert "ivb@nucleusteq.com" not in emails  # disabled interviewers are hidden
    assert "password" not in res.json()[0]

    # full user list stays admin only
    res = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403
