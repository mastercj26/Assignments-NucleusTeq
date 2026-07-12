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
            "email": "hr@nucleusteq.com",
            "password": hash_password("hrpass123"),
            "role": UserRole.HR,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )
    response = client.post(
        "/auth/login", json={"email": "hr@nucleusteq.com", "password": "hrpass123"}
    )
    return response.json()["access_token"]


def get_interviewer_token():
    db = Database.connect()
    db["users"].insert_one(
        {
            "email": "interviewer@nucleusteq.com",
            "password": hash_password("int123"),
            "role": UserRole.INTERVIEWER,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )
    response = client.post(
        "/auth/login", json={"email": "interviewer@nucleusteq.com", "password": "int123"}
    )
    return response.json()["access_token"]


def setup_data():
    admin_token = get_hr_token()

    for i in range(2):
        client.post(
            "/jobs/",
            json={
                "job_title": f"Job {i}",
                "job_details": f"Details {i}",
                "job_role": "Developer",
                "required_skills": ["Python"],
                "experience_required": 2,
                "employment_type": "Full Time",
                "location": "Remote",
                "status": "open",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    for i in range(3):
        client.post(
            "/candidates/",
            json={
                "first_name": ["Alpha", "Beta", "Gamma", "Delta", "Echo"][i],
                "last_name": "Test",
                "email": f"user{i}@nucleusteq.com",
                "mobile_number": f"12345678{i}0",
                "current_company": "Company",
                "total_experience": 2.0,
                "applied_job_id": "dummy_job_id",
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    job_resp = client.post(
        "/jobs/",
        json={
            "job_title": "Test Job",
            "job_details": "Details",
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
            "first_name": "Main",
            "last_name": "Candidate",
            "email": "main@nucleusteq.com",
            "mobile_number": "1234567899",
            "current_company": "Company",
            "total_experience": 3.0,
            "applied_job_id": job_id,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    candidate_id = cand_resp.json()["id"]

    db = Database.connect()
    int_res = db["users"].insert_one(
        {
            "email": "int@nucleusteq.com",
            "password": hash_password("int123"),
            "role": UserRole.INTERVIEWER,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )
    interviewer_id = str(int_res.inserted_id)

    for i in range(4):
        client.post(
            "/interviews/",
            json={
                "candidate_id": candidate_id,
                "job_id": job_id,
                "interview_date": "2026-07-15T10:00:00",
                "start_time": f"{9 + i:02d}:00",
            "end_time": f"{10 + i:02d}:00",
                "assigned_interviewer_id": interviewer_id,
                "focus_tech_areas": ["Python"],
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    db["candidates"].update_many(
        {"email": {"$in": ["user0@nucleusteq.com", "user1@nucleusteq.com"]}},
        {"$set": {"status": "SELECTED"}},
    )
    db["candidates"].update_one({"email": "user2@nucleusteq.com"}, {"$set": {"status": "REJECTED"}})

    return admin_token, interviewer_id


def test_hr_dashboard():
    token = get_admin_token()
    setup_data()
    response = client.get("/dashboard/hr", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs"] == 3
    assert data["total_candidates"] == 4
    assert data["scheduled_interviews"] == 4
    assert data["selected_candidates"] == 2
    assert data["rejected_candidates"] == 1


def test_interviewer_dashboard():

    admin_token = get_hr_token()
    db = Database.connect()
    int_res = db["users"].insert_one(
        {
            "email": "int@nucleusteq.com",
            "password": hash_password("int123"),
            "role": UserRole.INTERVIEWER,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
        }
    )
    interviewer_id = str(int_res.inserted_id)

    login = client.post("/auth/login", json={"email": "int@nucleusteq.com", "password": "int123"})
    int_token = login.json()["access_token"]

    job_resp = client.post(
        "/jobs/",
        json={
            "job_title": "Test Job",
            "job_details": "Details",
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
            "first_name": "Main",
            "last_name": "Candidate",
            "email": "main@nucleusteq.com",
            "mobile_number": "1234567899",
            "current_company": "Company",
            "total_experience": 3.0,
            "applied_job_id": job_id,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    candidate_id = cand_resp.json()["id"]

    for i in range(3):
        client.post(
            "/interviews/",
            json={
                "candidate_id": candidate_id,
                "job_id": job_id,
                "interview_date": "2026-07-15T10:00:00",
                "start_time": f"{9 + i:02d}:00",
            "end_time": f"{10 + i:02d}:00",
                "assigned_interviewer_id": interviewer_id,
                "focus_tech_areas": ["Python"],
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    db["interviews"].update_one(
        {"assigned_interviewer_id": interviewer_id}, {"$set": {"status": "completed"}}
    )

    response = client.get(
        "/dashboard/interviewer", headers={"Authorization": f"Bearer {int_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["assigned_interviews"] == 3
    assert data["pending_feedback"] == 2
    assert data["completed_feedback"] == 1


def test_dashboard_unauthorized_role():

    token = get_interviewer_token()
    response = client.get("/dashboard/hr", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

    hr_token = get_hr_token()
    response = client.get("/dashboard/interviewer", headers={"Authorization": f"Bearer {hr_token}"})
    assert response.status_code == 403
