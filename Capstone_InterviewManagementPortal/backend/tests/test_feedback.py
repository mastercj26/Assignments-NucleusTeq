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
    for coll in ["users", "candidates", "job_descriptions", "interviews", "feedbacks"]:
        db[coll].delete_many({})
    yield
    for coll in ["users", "candidates", "job_descriptions", "interviews", "feedbacks"]:
        db[coll].delete_many({})


def get_admin_token():
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "admin@nucleusteq.com",
            "password": hash_password("admin123"),
            "role": UserRole.ADMIN,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )
    response = client.post(
        "/auth/login", json={"email": "admin@nucleusteq.com", "password": "admin123"}
    )
    return response.json()["access_token"]


def get_hr_token():
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "hrfeedback@nucleusteq.com",
            "password": hash_password("hrpass123"),
            "role": UserRole.HR,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )
    response = client.post(
        "/auth/login", json={"email": "hrfeedback@nucleusteq.com", "password": "hrpass123"}
    )
    return response.json()["access_token"]


def get_interviewer_token_and_id():
    db = Database.connect()
    user = {
        "email": "interviewer@nucleusteq.com",
        "password": hash_password("int123"),
        "role": UserRole.INTERVIEWER,
        "status": UserStatus.ACTIVE,
        "is_first_login": False,
    }
    result = db["users"].insert_one(user)
    user_id = str(result.inserted_id)
    response = client.post(
        "/auth/login", json={"email": "interviewer@nucleusteq.com", "password": "int123"}
    )
    return response.json()["access_token"], user_id


def create_interview_for_interviewer():
    admin_token = get_hr_token()

    job_resp = client.post(
        "/jobs/",
        json={
            "job_title": "Test Job",
            "job_details": "Test details",
            "job_role": "Developer",
            "required_skills": ["Python"],
            "experience_required": 2,
            "employment_type": "Full Time",
            "location": "Remote",
            "status": "open",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    job_id = job_resp.json()["id"]

    cand_resp = client.post(
        "/candidates/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@nucleusteq.com",
            "mobile_number": "1234567890",
            "current_company": "Google",
            "total_experience": 5.5,
            "applied_job_id": job_id,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    candidate_id = cand_resp.json()["id"]

    int_token, int_id = get_interviewer_token_and_id()

    int_resp = client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "start_time": "10:00",
        "end_time": "11:00",
            "assigned_interviewer_id": int_id,
            "focus_tech_areas": ["Python", "FastAPI"],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    interview_id = int_resp.json()["id"]
    return int_token, interview_id, int_id


def test_submit_feedback_success():
    int_token, interview_id, _ = create_interview_for_interviewer()
    response = client.post(
        "/feedbacks/",
        json={
            "interview_id": interview_id,
            "technical_rating": 4,
            "communication_rating": 5,
            "problem_solving_rating": 4,
            "tech_areas_covered": ["Python", "FastAPI"],
            "comments": "Good performance",
            "recommendation": "SELECT",
        },
        headers={"Authorization": f"Bearer {int_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["technical_rating"] == 4
    assert data["recommendation"] == "SELECT"
    assert data["interview_id"] == interview_id


def test_submit_feedback_invalid_rating():
    int_token, interview_id, _ = create_interview_for_interviewer()
    response = client.post(
        "/feedbacks/",
        json={
            "interview_id": interview_id,
            "technical_rating": 6,
            "communication_rating": 5,
            "problem_solving_rating": 4,
            "tech_areas_covered": ["Python"],
            "comments": "Good",
            "recommendation": "NEXT_ROUND",
        },
        headers={"Authorization": f"Bearer {int_token}"},
    )
    assert response.status_code == 422


def test_submit_feedback_not_assigned():

    admin_token = get_hr_token()

    db = Database.connect()
    other = db["users"].insert_one(
        {
            "email": "other@nucleusteq.com",
            "password": hash_password("other123"),
            "role": UserRole.INTERVIEWER,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )
    other_id = str(other.inserted_id)

    login = client.post(
        "/auth/login", json={"email": "other@nucleusteq.com", "password": "other123"}
    )
    other_token = login.json()["access_token"]

    int_token, interview_id, _ = create_interview_for_interviewer()

    response = client.post(
        "/feedbacks/",
        json={
            "interview_id": interview_id,
            "technical_rating": 4,
            "communication_rating": 4,
            "problem_solving_rating": 4,
            "tech_areas_covered": ["Python"],
            "comments": "OK",
            "recommendation": "REJECT",
        },
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 403
    assert "not assigned" in response.text


def test_submit_feedback_duplicate():
    int_token, interview_id, _ = create_interview_for_interviewer()

    client.post(
        "/feedbacks/",
        json={
            "interview_id": interview_id,
            "technical_rating": 4,
            "communication_rating": 4,
            "problem_solving_rating": 4,
            "tech_areas_covered": ["Python"],
            "comments": "OK",
            "recommendation": "NEXT_ROUND",
        },
        headers={"Authorization": f"Bearer {int_token}"},
    )

    response = client.post(
        "/feedbacks/",
        json={
            "interview_id": interview_id,
            "technical_rating": 5,
            "communication_rating": 5,
            "problem_solving_rating": 5,
            "tech_areas_covered": ["Python"],
            "comments": "Better",
            "recommendation": "SELECT",
        },
        headers={"Authorization": f"Bearer {int_token}"},
    )
    assert response.status_code == 409
    assert "already submitted" in response.text


def test_get_feedback_success():
    int_token, interview_id, _ = create_interview_for_interviewer()
    client.post(
        "/feedbacks/",
        json={
            "interview_id": interview_id,
            "technical_rating": 4,
            "communication_rating": 4,
            "problem_solving_rating": 4,
            "tech_areas_covered": ["Python"],
            "comments": "OK",
            "recommendation": "NEXT_ROUND",
        },
        headers={"Authorization": f"Bearer {int_token}"},
    )
    response = client.get(
        f"/feedbacks/interview/{interview_id}", headers={"Authorization": f"Bearer {int_token}"}
    )
    assert response.status_code == 200
    assert response.json()["interview_id"] == interview_id


def test_get_feedback_not_found():
    int_token, _, _ = create_interview_for_interviewer()
    response = client.get(
        "/feedbacks/interview/unknown_id", headers={"Authorization": f"Bearer {int_token}"}
    )
    assert response.status_code == 404
