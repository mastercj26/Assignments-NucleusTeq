import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Database
from src.core.security import hash_password, create_access_token
from src.enums.user_enums import UserRole, UserStatus

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    db = Database.connect()
    db["users"].delete_many({})
    db["candidates"].delete_many({})
    yield
    db["users"].delete_many({})
    db["candidates"].delete_many({})

def get_admin_token():
    db = Database.connect()
    db["users"].insert_one({
        "email": "admin@nucleusteq.com",
        "password": hash_password("admin123"),
        "role": UserRole.ADMIN,
        "status": UserStatus.ACTIVE,
        "is_first_login": False
    })
    response = client.post("/auth/login", json={
        "email": "admin@nucleusteq.com",
        "password": "admin123"
    })
    return response.json()["access_token"]

def get_hr_token():
    db = Database.connect()
    db["users"].insert_one({
        "email": "hr@nucleusteq.com",
        "password": hash_password("hrpass123"),
        "role": UserRole.HR,
        "status": UserStatus.ACTIVE,
        "is_first_login": False
    })
    response = client.post("/auth/login", json={
        "email": "hr@nucleusteq.com",
        "password": "hrpass123"
    })
    return response.json()["access_token"]

def test_create_candidate_success():
    token = get_admin_token()
    # Create a job first (needed for applied_job_id)
    # For simplicity, we'll mock a job ID or just use a dummy ObjectId
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"  # dummy
    response = client.post(
        "/candidates/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@nucleusteq.com",
            "mobile_number": "1234567890",
            "current_company": "Google",
            "total_experience": 5.5,
            "applied_job_id": job_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["email"] == "john@nucleusteq.com"
    assert data["status"] == "PROFILE_CREATED"

def test_create_candidate_duplicate_email():
    token = get_admin_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"
    # Create first candidate
    client.post(
        "/candidates/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@nucleusteq.com",
            "mobile_number": "1234567890",
            "current_company": "Google",
            "total_experience": 5.5,
            "applied_job_id": job_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    # Create another with same email
    response = client.post(
        "/candidates/",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "john@nucleusteq.com",
            "mobile_number": "0987654321",
            "current_company": "Microsoft",
            "total_experience": 3.0,
            "applied_job_id": job_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 409
    assert "Email already exists" in response.text

def test_create_candidate_duplicate_mobile():
    token = get_admin_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"
    client.post(
        "/candidates/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@nucleusteq.com",
            "mobile_number": "1234567890",
            "current_company": "Google",
            "total_experience": 5.5,
            "applied_job_id": job_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.post(
        "/candidates/",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@nucleusteq.com",
            "mobile_number": "1234567890",
            "current_company": "Microsoft",
            "total_experience": 3.0,
            "applied_job_id": job_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 409
    assert "Mobile number already exists" in response.text

def test_create_candidate_invalid_domain():
    token = get_admin_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"
    response = client.post(
        "/candidates/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@gmail.com",
            "mobile_number": "1234567890",
            "current_company": "Google",
            "total_experience": 5.5,
            "applied_job_id": job_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422
    assert "nucleusteq.com" in response.text

def test_update_candidate_success():
    token = get_admin_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"
    # Create candidate
    create_resp = client.post(
        "/candidates/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@nucleusteq.com",
            "mobile_number": "1234567890",
            "current_company": "Google",
            "total_experience": 5.5,
            "applied_job_id": job_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    cand_id = create_resp.json()["id"]

    # Update
    response = client.put(
        f"/candidates/{cand_id}",
        json={
            "first_name": "Jonathan",
            "total_experience": 6.0
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jonathan"
    assert data["total_experience"] == 6.0

def test_list_candidates():
    token = get_admin_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"
    # Create a few candidates
    for i in range(3):
        client.post(
            "/candidates/",
            json={
                "first_name": f"User{i}",
                "last_name": "Test",
                "email": f"user{i}@nucleusteq.com",
                "mobile_number": f"12345678{i}0",
                "current_company": "Company",
                "total_experience": 2.0,
                "applied_job_id": job_id
            },
            headers={"Authorization": f"Bearer {token}"}
        )
    response = client.get("/candidates/?page=1&per_page=2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["candidates"]) == 2
    assert data["total"] == 3
    assert data["pages"] == 2