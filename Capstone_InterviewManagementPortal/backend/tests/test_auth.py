import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Database
from src.core.security import hash_password
from src.enums.user_enums import UserRole, UserStatus

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_users():
    """Clean the users collection before and after each test."""
    db = Database.connect()
    db["users"].delete_many({})
    yield
    db["users"].delete_many({})


def test_login_success():
    """Test successful login with valid credentials."""
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

    response = client.post(
        "/auth/login", json={"email": "hr@nucleusteq.com", "password": "hrpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "hr@nucleusteq.com"
    assert data["role"] == UserRole.HR


def test_login_first_login_required():
    """User with is_first_login=True must reset password."""
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "new@nucleusteq.com",
            "password": hash_password("new123"),
            "role": UserRole.INTERVIEWER,
            "status": UserStatus.FIRST_LOGIN,
            "is_first_login": True,
        }
    )

    response = client.post(
        "/auth/login", json={"email": "new@nucleusteq.com", "password": "new123"}
    )
    assert response.status_code == 401
    assert "reset your password" in response.json()["message"].lower()


def test_login_invalid_credentials():
    """Login with wrong password should fail."""
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "wrong@nucleusteq.com",
            "password": hash_password("correct123"),
            "role": UserRole.HR,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )

    response = client.post(
        "/auth/login", json={"email": "wrong@nucleusteq.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert "invalid" in response.json()["message"].lower()


def test_login_nonexistent_user():
    """Login with email not in DB."""
    response = client.post(
        "/auth/login", json={"email": "nonexistent@nucleusteq.com", "password": "anypass"}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()


def test_reset_password_success():
    """Successful password reset."""
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "reset@nucleusteq.com",
            "password": hash_password("oldPass123"),
            "role": UserRole.HR,
            "status": UserStatus.FIRST_LOGIN,
            "is_first_login": True,
        }
    )

    response = client.post(
        "/auth/reset-password",
        json={
            "email": "reset@nucleusteq.com",
            "old_password": "oldPass123",
            "new_password": "newPass@1",
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset successfully"

    # Verify that is_first_login is now False and status changed
    user = db["users"].find_one({"email": "reset@nucleusteq.com"})
    assert user["is_first_login"] is False
    assert user["status"] == UserStatus.ACTIVE


def test_reset_password_wrong_old_password():
    """Reset with incorrect old password should fail."""
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "resetwrong@nucleusteq.com",
            "password": hash_password("correctOld"),
            "role": UserRole.HR,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )

    response = client.post(
        "/auth/reset-password",
        json={
            "email": "resetwrong@nucleusteq.com",
            "old_password": "wrongOld",
            "new_password": "newPass@1",
        },
    )
    assert response.status_code == 401
    assert "invalid" in response.json()["message"].lower()


def test_reset_password_email_not_found():
    """Reset for non-existing email."""
    response = client.post(
        "/auth/reset-password",
        json={
            "email": "missing@nucleusteq.com",
            "old_password": "anything",
            "new_password": "newPass@1",
        },
    )
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()


def test_login_missing_fields():
    """Login without required fields should fail with 422."""
    response = client.post("/auth/login", json={"email": "hr@nucleusteq.com"})
    assert response.status_code == 422

    response = client.post("/auth/login", json={})
    assert response.status_code == 422


def test_reset_password_old_password_stops_working():
    """Old password should stop working after reset."""
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "rotate@nucleusteq.com",
            "password": hash_password("oldpass1!"),
            "role": UserRole.HR,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )

    response = client.post(
        "/auth/reset-password",
        json={
            "email": "rotate@nucleusteq.com",
            "old_password": "oldpass1!",
            "new_password": "newpass2@",
        },
    )
    assert response.status_code == 200

    # Old password must be rejected
    response = client.post(
        "/auth/login", json={"email": "rotate@nucleusteq.com", "password": "oldpass1!"}
    )
    assert response.status_code == 401

    # New password must work
    response = client.post(
        "/auth/login", json={"email": "rotate@nucleusteq.com", "password": "newpass2@"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_password_is_hashed_in_db():
    """Password in DB should be hashed, not plaintext."""
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "hashcheck@nucleusteq.com",
            "password": hash_password("secret1!"),
            "role": UserRole.HR,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )
    stored = db["users"].find_one({"email": "hashcheck@nucleusteq.com"})["password"]
    assert stored != "secret1!"
    assert stored.startswith("$2")  # bcrypt marker
