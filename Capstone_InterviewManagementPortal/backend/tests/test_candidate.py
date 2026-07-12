import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Database
from src.core.security import hash_password
from src.enums.user_enums import UserRole, UserStatus

client = TestClient(app)

# Test data
CANDIDATE_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@nucleusteq.com",
    "mobile_number": "1234567890",
    "current_company": "Google",
    "total_experience": 5.5,
    "applied_job_id": "64b8f2a1c9d3e4f5a6b7c8d9",  # dummy job ID
}


@pytest.fixture(autouse=True)
def clean_db():
    db = Database.connect()
    db["users"].delete_many({})
    db["candidates"].delete_many({})
    db["job_descriptions"].delete_many({})
    yield
    db["users"].delete_many({})
    db["candidates"].delete_many({})
    db["job_descriptions"].delete_many({})


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


def test_create_candidate_success():
    token = get_hr_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"  # dummy
    response = client.post(
        "/candidates/", json=CANDIDATE_DATA, headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["email"] == "john@nucleusteq.com"
    assert data["status"] == "PROFILE_CREATED"


def test_create_candidate_duplicate_email():
    token = get_hr_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"
    # Create first candidate
    client.post("/candidates/", json=CANDIDATE_DATA, headers={"Authorization": f"Bearer {token}"})
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
            "applied_job_id": job_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409
    assert "Email already exists" in response.text


def test_create_candidate_duplicate_mobile():
    token = get_hr_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"
    client.post("/candidates/", json=CANDIDATE_DATA, headers={"Authorization": f"Bearer {token}"})
    response = client.post(
        "/candidates/",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@nucleusteq.com",
            "mobile_number": "1234567890",
            "current_company": "Microsoft",
            "total_experience": 3.0,
            "applied_job_id": job_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 409
    assert "Mobile number already exists" in response.text


def test_create_candidate_invalid_domain():
    token = get_hr_token()
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
            "applied_job_id": job_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422
    assert "nucleusteq.com" in response.text


def test_update_candidate_success():
    token = get_hr_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"
    # Create candidate
    create_resp = client.post(
        "/candidates/", json=CANDIDATE_DATA, headers={"Authorization": f"Bearer {token}"}
    )
    cand_id = create_resp.json()["id"]

    # Update
    response = client.put(
        f"/candidates/{cand_id}",
        json={"first_name": "Jonathan", "total_experience": 6.0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jonathan"
    assert data["total_experience"] == 6.0


def test_list_candidates():
    token = get_hr_token()
    job_id = "64b8f2a1c9d3e4f5a6b7c8d9"

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
                "applied_job_id": job_id,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    response = client.get(
        "/candidates/?page=1&per_page=2", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["candidates"]) == 2
    assert data["total"] == 3
    assert data["pages"] == 2


def test_upload_resume_success():
    token = get_hr_token()
    # Create a candidate
    resp = client.post(
        "/candidates/", json=CANDIDATE_DATA, headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201
    candidate_id = resp.json()["id"]

    # Upload a dummy PDF
    dummy_pdf = b"%PDF-1.4\n" + b"0" * 500
    response = client.post(
        f"/candidates/{candidate_id}/resume",
        files={"file": ("resume.pdf", dummy_pdf, "application/pdf")},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "resume.pdf"


def test_status_update():
    token = get_hr_token()
    # Create candidate
    resp = client.post(
        "/candidates/", json=CANDIDATE_DATA, headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201
    candidate_id = resp.json()["id"]

    # Update status
    response = client.patch(
        f"/candidates/{candidate_id}/status",
        json={"status": "INTERVIEW_SCHEDULED", "notes": "First round scheduled"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    # Verify history
    hist = client.get(
        f"/candidates/{candidate_id}/status-history", headers={"Authorization": f"Bearer {token}"}
    )
    assert hist.status_code == 200
    # first entry is PROFILE_CREATED which gets added on creation
    history = hist.json()["history"]
    assert len(history) == 2
    assert history[0]["status"] == "PROFILE_CREATED"
    assert history[1]["status"] == "INTERVIEW_SCHEDULED"
    assert hist.json()["history"][-1]["status"] == "INTERVIEW_SCHEDULED"


def test_resume_download_permissions():
    """Resume download is allowed for HR and the assigned interviewer only."""
    hr_token = get_hr_token()
    admin_token = get_admin_token()

    db = Database.connect()

    def make_interviewer(email):
        result = db["users"].insert_one(
            {
                "email": email,
                "password": hash_password("ivpass123"),
                "role": UserRole.INTERVIEWER,
                "status": UserStatus.ACTIVE,
                "is_first_login": False,
            }
        )
        token = client.post(
            "/auth/login", json={"email": email, "password": "ivpass123"}
        ).json()["access_token"]
        return token, str(result.inserted_id)

    assigned_token, assigned_id = make_interviewer("assigned@nucleusteq.com")
    other_token, _ = make_interviewer("other@nucleusteq.com")

    hr_auth = {"Authorization": f"Bearer {hr_token}"}
    job = client.post("/jobs/", json={
        "job_title": "Backend Engineer",
        "job_details": "Python role",
        "job_role": "Developer",
        "required_skills": ["Python"],
        "experience_required": 3,
        "employment_type": "Full Time",
        "location": "Indore",
    }, headers=hr_auth)
    job_id = job.json()["id"]

    resp = client.post("/candidates/", json=CANDIDATE_DATA, headers=hr_auth)
    candidate_id = resp.json()["id"]

    dummy_pdf = b"%PDF-1.4\n" + b"0" * 500
    resp = client.post(
        f"/candidates/{candidate_id}/resume",
        files={"file": ("resume.pdf", dummy_pdf, "application/pdf")},
        headers=hr_auth,
    )
    assert resp.status_code == 200

    # Assign one interviewer to this candidate
    resp = client.post("/interviews/", json={
        "candidate_id": candidate_id,
        "job_id": job_id,
        "interview_date": "2026-08-01T10:00:00",
        "interview_time": "10:00 AM",
        "assigned_interviewer_id": assigned_id,
        "focus_tech_areas": ["Python"],
    }, headers=hr_auth)
    assert resp.status_code == 201

    # HR and the assigned interviewer can download
    for token in (hr_token, assigned_token):
        resp = client.get(
            f"/candidates/{candidate_id}/resume", headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 200
        assert resp.content.startswith(b"%PDF")

    # Unassigned interviewer and admin cannot
    for token in (other_token, admin_token):
        resp = client.get(
            f"/candidates/{candidate_id}/resume", headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 403

    # Interviewers cannot upload
    resp = client.post(
        f"/candidates/{candidate_id}/resume",
        files={"file": ("resume2.pdf", dummy_pdf, "application/pdf")},
        headers={"Authorization": f"Bearer {assigned_token}"},
    )
    assert resp.status_code == 403


def test_upload_resume_rejects_bad_files():
    """Invalid files should get rejected with 422."""
    token = get_hr_token()
    resp = client.post(
        "/candidates/", json=CANDIDATE_DATA, headers={"Authorization": f"Bearer {token}"}
    )
    candidate_id = resp.json()["id"]
    auth = {"Authorization": f"Bearer {token}"}

    # Wrong extension
    resp = client.post(
        f"/candidates/{candidate_id}/resume",
        files={"file": ("resume.docx", b"%PDF" + b"0" * 500, "application/pdf")},
        headers=auth,
    )
    assert resp.status_code == 422

    # Empty file
    resp = client.post(
        f"/candidates/{candidate_id}/resume",
        files={"file": ("resume.pdf", b"", "application/pdf")},
        headers=auth,
    )
    assert resp.status_code == 422

    # Too small to be a real document
    resp = client.post(
        f"/candidates/{candidate_id}/resume",
        files={"file": ("resume.pdf", b"%PDF", "application/pdf")},
        headers=auth,
    )
    assert resp.status_code == 422

    # Right size but not actually a PDF
    resp = client.post(
        f"/candidates/{candidate_id}/resume",
        files={"file": ("resume.pdf", b"not a pdf " * 20, "application/pdf")},
        headers=auth,
    )
    assert resp.status_code == 422

    # Over the 10MB limit
    resp = client.post(
        f"/candidates/{candidate_id}/resume",
        files={"file": ("resume.pdf", b"%PDF" + b"0" * (10 * 1024 * 1024 + 1), "application/pdf")},
        headers=auth,
    )
    assert resp.status_code == 422


def test_update_candidate_persists_to_db():
    """Check the update actually reached the DB."""
    token = get_hr_token()
    resp = client.post(
        "/candidates/", json=CANDIDATE_DATA, headers={"Authorization": f"Bearer {token}"}
    )
    candidate_id = resp.json()["id"]

    resp = client.put(
        f"/candidates/{candidate_id}",
        json={"current_company": "Acme Corp", "total_experience": 7.5},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200

    from bson import ObjectId

    db = Database.connect()
    doc = db["candidates"].find_one({"_id": ObjectId(candidate_id)})
    assert doc is not None
    assert doc["current_company"] == "Acme Corp"
    assert doc["total_experience"] == 7.5


def test_create_candidate_rejects_special_chars():
    token = get_hr_token()
    auth = {"Authorization": f"Bearer {token}"}

    res = client.post("/candidates/", json={**CANDIDATE_DATA, "first_name": "John#"}, headers=auth)
    assert res.status_code == 422

    res = client.post("/candidates/", json={**CANDIDATE_DATA, "email": "jo$hn@nucleusteq.com"}, headers=auth)
    assert res.status_code == 422


def test_candidates_listed_newest_first():
    token = get_hr_token()
    auth = {"Authorization": f"Bearer {token}"}

    for i, name in enumerate(["Older", "Newer"]):
        res = client.post("/candidates/", json={
            **CANDIDATE_DATA,
            "first_name": name,
            "email": f"order{i}@nucleusteq.com",
            "mobile_number": f"90000000{i:02d}",
        }, headers=auth)
        assert res.status_code == 201

    res = client.get("/candidates/", headers=auth)
    names = [c["first_name"] for c in res.json()["candidates"]]
    assert names.index("Newer") < names.index("Older")
