import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Database
from src.core.security import hash_password
from src.enums.user_enums import UserRole, UserStatus
from src.enums.candidate_enums import CandidateStatus

client = TestClient(app)


JOB_DATA = {
    "job_title": "Test Job",
    "job_details": "Test details",
    "job_role": "Developer",
    "required_skills": ["Python"],
    "experience_required": 2,
    "employment_type": "Full Time",
    "location": "Remote",
    "status": "open"
}
CANDIDATE_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@nucleusteq.com",
    "mobile_number": "1234567890",
    "current_company": "Google",
    "total_experience": 5.5,
    "applied_job_id": "dummy_job_id"  
}

@pytest.fixture(autouse=True)
def clean_db():
    db = Database.connect()
    for coll in ["users", "candidates", "jobs", "interviews", "feedbacks"]:
        db[coll].delete_many({})
    yield
    for coll in ["users", "candidates", "jobs", "interviews", "feedbacks"]:
        db[coll].delete_many({})

def get_admin_token():
    db = Database.connect()
    db["users"].insert_one({
        "email": "admin@nucleusteq.com",
        "password": hash_password("admin123"),
        "role": UserRole.ADMIN,
        "status": UserStatus.ACTIVE,
        "is_first_login": False
    })
    response = client.post("/auth/login", json={"email": "admin@nucleusteq.com", "password": "admin123"})
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
    response = client.post("/auth/login", json={"email": "hr@nucleusteq.com", "password": "hrpass123"})
    return response.json()["access_token"]

def get_interviewer_token():
    db = Database.connect()
    db["users"].insert_one({
        "email": "interviewer@nucleusteq.com",
        "password": hash_password("int123"),
        "role": UserRole.INTERVIEWER,
        "status": UserStatus.ACTIVE,
        "is_first_login": False
    })
    response = client.post("/auth/login", json={"email": "interviewer@nucleusteq.com", "password": "int123"})
    return response.json()["access_token"]

def create_job(token):
    response = client.post("/jobs/", json=JOB_DATA, headers={"Authorization": f"Bearer {token}"})
    return response.json()["id"]

def create_candidate(token, job_id):
    data = CANDIDATE_DATA.copy()
    data["applied_job_id"] = job_id
    response = client.post("/candidates/", json=data, headers={"Authorization": f"Bearer {token}"})
    return response.json()["id"]

def get_interviewer_id(token):
   
    db = Database.connect()
    user = db["users"].find_one({"email": "interviewer@nucleusteq.com"})
    return user["_id"]

def test_schedule_interview_success():
    token = get_admin_token()
    job_id = create_job(token)
    candidate_id = create_candidate(token, job_id)
    interviewer_id = get_interviewer_id(token)

    response = client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python", "FastAPI"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["candidate_id"] == candidate_id
    assert data["status"] == "scheduled"
    
    cand = client.get(f"/candidates/{candidate_id}", headers={"Authorization": f"Bearer {token}"})
    assert cand.json()["status"] == "INTERVIEW_SCHEDULED"

def test_schedule_interview_invalid_candidate():
    token = get_admin_token()
    job_id = create_job(token)
    interviewer_id = get_interviewer_id(token)

    response = client.post(
        "/interviews/",
        json={
            "candidate_id": "invalid_id",
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400

def test_schedule_interview_unauthorized_role():
    token = get_interviewer_token() 
    job_id = create_job(get_admin_token())  
    candidate_id = create_candidate(get_admin_token(), job_id)
    interviewer_id = get_interviewer_id(token)

    response = client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

def test_list_interviews_as_hr():
    token = get_hr_token()
    # Create some interviews
    admin_token = get_admin_token()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)
    interviewer_id = get_interviewer_id(admin_token)
    for _ in range(3):
        client.post(
            "/interviews/",
            json={
                "candidate_id": candidate_id,
                "job_id": job_id,
                "interview_date": "2026-07-15T10:00:00",
                "interview_time": "10:00 AM",
                "assigned_interviewer_id": interviewer_id,
                "focus_tech_areas": ["Python"]
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )

    response = client.get("/interviews/?page=1&per_page=2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["interviews"]) == 2
    assert data["total"] == 3
    assert data["pages"] == 2

def test_list_interviews_as_interviewer_filtered():
   
    interviewer_token = get_interviewer_token()
    interviewer_id = get_interviewer_id(interviewer_token)

    
    admin_token = get_admin_token()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)

   
    client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
   
    db = Database.connect()
    other = db["users"].insert_one({
        "email": "other@nucleusteq.com",
        "password": hash_password("other123"),
        "role": UserRole.INTERVIEWER,
        "status": UserStatus.ACTIVE,
        "is_first_login": False
    })
    other_id = str(other.inserted_id)
    client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-16T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": other_id,
            "focus_tech_areas": ["JavaScript"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get("/interviews/", headers={"Authorization": f"Bearer {interviewer_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["interviews"][0]["assigned_interviewer_id"] == interviewer_id

def test_get_interview_success():
    admin_token = get_admin_token()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)
    interviewer_id = get_interviewer_id(admin_token)

    create_resp = client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    interview_id = create_resp.json()["id"]

    response = client.get(f"/interviews/{interview_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == interview_id

def test_get_interview_denied_for_other_interviewer():
    admin_token = get_admin_token()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)
    interviewer_id = get_interviewer_id(admin_token)

    create_resp = client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python"]
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    interview_id = create_resp.json()["id"]

    
    db = Database.connect()
    db["users"].insert_one({
        "email": "other_interviewer@nucleusteq.com",
        "password": hash_password("int456"),
        "role": UserRole.INTERVIEWER,
        "status": UserStatus.ACTIVE,
        "is_first_login": False
    })
    login = client.post("/auth/login", json={"email": "other_interviewer@nucleusteq.com", "password": "int456"})
    other_token = login.json()["access_token"]

    response = client.get(f"/interviews/{interview_id}", headers={"Authorization": f"Bearer {other_token}"})
    assert response.status_code == 403