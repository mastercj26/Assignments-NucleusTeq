import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Database
from src.core.security import hash_password
from src.enums.user_enums import UserRole, UserStatus

client = TestClient(app)

JOB_DATA = {
    "job_title": "Test Job",
    "job_details": "Test details",
    "job_role": "Developer",
    "required_skills": ["Python"],
    "experience_required": 2,
    "employment_type": "Full Time",
    "location": "Remote",
    "status": "open",
}


@pytest.fixture(autouse=True)
def clean_db():
    db = Database.connect()
    for coll in ["users", "candidates", "job_descriptions", "interviews", "feedbacks"]:
        db[coll].delete_many({})
    yield
    for coll in ["users", "candidates", "job_descriptions", "interviews", "feedbacks"]:
        db[coll].delete_many({})


def _insert_user(email, role, password="pass123!"):
    db = Database.connect()
    result = db["users"].insert_one(
        {
            "email": email,
            "password": hash_password(password),
            "role": role,
            "status": UserStatus.ACTIVE,
            "is_first_login": False,
            "first_name": role.capitalize(),
            "last_name": "User",
        }
    )
    return str(result.inserted_id)


def _login(email, password="pass123!"):
    res = client.post("/auth/login", json={"email": email, "password": password})
    return res.json()["access_token"]


def get_admin_token():
    _insert_user("admin@nucleusteq.com", UserRole.ADMIN)
    return _login("admin@nucleusteq.com")


def get_hr_token():
    _insert_user("hr@nucleusteq.com", UserRole.HR)
    return _login("hr@nucleusteq.com")


def get_interviewer_token_and_id():
    user_id = _insert_user("interviewer@nucleusteq.com", UserRole.INTERVIEWER)
    token = _login("interviewer@nucleusteq.com")
    return token, user_id


def create_job(token):
    res = client.post("/jobs/", json=JOB_DATA, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 201
    return res.json()["id"]


def create_candidate(token, job_id):
    res = client.post(
        "/candidates/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@nucleusteq.com",
            "mobile_number": "1234567890",
            "total_experience": 5.0,
            "applied_job_id": job_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 201
    return res.json()["id"]


def test_schedule_interview_success():
    admin_token = get_hr_token()
    interviewer_token, interviewer_id = get_interviewer_token_and_id()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)

    res = client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python", "FastAPI"],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert res.status_code == 201
    data = res.json()
    assert data["candidate_id"] == candidate_id
    assert data["status"] == "scheduled"

    cand = client.get(
        f"/candidates/{candidate_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert cand.json()["status"] == "INTERVIEW_SCHEDULED"


def test_schedule_interview_invalid_candidate():
    admin_token = get_hr_token()
    _, interviewer_id = get_interviewer_token_and_id()
    job_id = create_job(admin_token)

    res = client.post(
        "/interviews/",
        json={
            "candidate_id": "000000000000000000000000",
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python"],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert res.status_code == 404


def test_schedule_interview_unauthorized_role():
    admin_token = get_hr_token()
    interviewer_token, interviewer_id = get_interviewer_token_and_id()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)

    res = client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python"],
        },
        headers={"Authorization": f"Bearer {interviewer_token}"},
    )

    assert res.status_code == 403


def test_list_interviews_as_hr():
    admin_token = get_hr_token()
    hr_token = admin_token
    _, interviewer_id = get_interviewer_token_and_id()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)

    for idx in range(3):
        client.post(
            "/interviews/",
            json={
                "candidate_id": candidate_id,
                "job_id": job_id,
                "interview_date": "2026-07-15T10:00:00",
                "interview_time": f"{9 + idx}:00 AM",
                "assigned_interviewer_id": interviewer_id,
                "focus_tech_areas": ["Python"],
            },
            headers={"Authorization": f"Bearer {admin_token}"},
        )

    res = client.get(
        "/interviews/?page=1&per_page=2", headers={"Authorization": f"Bearer {hr_token}"}
    )
    assert res.status_code == 200
    data = res.json()
    assert len(data["interviews"]) == 2
    assert data["total"] == 3
    assert data["pages"] == 2


def test_list_interviews_as_interviewer_filtered():
    admin_token = get_hr_token()
    interviewer_token, interviewer_id = get_interviewer_token_and_id()
    other_id = _insert_user("other@nucleusteq.com", UserRole.INTERVIEWER)

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
            "focus_tech_areas": ["Python"],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-16T10:00:00",
            "interview_time": "11:00 AM",
            "assigned_interviewer_id": other_id,
            "focus_tech_areas": ["JavaScript"],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    res = client.get("/interviews/", headers={"Authorization": f"Bearer {interviewer_token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 1
    assert data["interviews"][0]["assigned_interviewer_id"] == interviewer_id


def test_get_interview_success():
    admin_token = get_hr_token()
    _, interviewer_id = get_interviewer_token_and_id()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)

    create_res = client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python"],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    interview_id = create_res.json()["id"]

    res = client.get(
        f"/interviews/{interview_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200
    assert res.json()["id"] == interview_id


def test_get_interview_denied_for_other_interviewer():
    admin_token = get_hr_token()
    _, interviewer_id = get_interviewer_token_and_id()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)

    create_res = client.post(
        "/interviews/",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
            "interview_date": "2026-07-15T10:00:00",
            "interview_time": "10:00 AM",
            "assigned_interviewer_id": interviewer_id,
            "focus_tech_areas": ["Python"],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    interview_id = create_res.json()["id"]

    _insert_user("other@nucleusteq.com", UserRole.INTERVIEWER)
    other_token = _login("other@nucleusteq.com")

    res = client.get(
        f"/interviews/{interview_id}", headers={"Authorization": f"Bearer {other_token}"}
    )
    assert res.status_code == 403


def test_schedule_interview_slot_conflict():
    """Same interviewer + same slot should give 409."""
    admin_token = get_hr_token()
    _, interviewer_id = get_interviewer_token_and_id()
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)

    payload = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "interview_date": "2026-07-20T10:00:00",
        "interview_time": "10:00 AM",
        "assigned_interviewer_id": interviewer_id,
        "focus_tech_areas": ["Python"],
    }
    res = client.post(
        "/interviews/", json=payload, headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 201

    res = client.post(
        "/interviews/", json=payload, headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 409
    assert "time slot" in res.json()["message"].lower()

    # different time should work
    res = client.post(
        "/interviews/",
        json={**payload, "interview_time": "2:00 PM"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 201


def test_reassign_interviewer_slot_conflict():
    """Reassigning to a busy interviewer should give 409."""
    admin_token = get_hr_token()
    _, interviewer_a = get_interviewer_token_and_id()
    interviewer_b = _insert_user("interviewer2@nucleusteq.com", UserRole.INTERVIEWER)
    job_id = create_job(admin_token)
    candidate_id = create_candidate(admin_token, job_id)

    base = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "interview_date": "2026-07-21T10:00:00",
        "interview_time": "11:00 AM",
        "focus_tech_areas": ["Python"],
    }
    res = client.post(
        "/interviews/",
        json={**base, "assigned_interviewer_id": interviewer_a},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 201

    res = client.post(
        "/interviews/",
        json={**base, "assigned_interviewer_id": interviewer_b},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 201
    second_id = res.json()["id"]

    # A is already busy at this slot
    res = client.put(
        f"/interviews/{second_id}",
        json={"assigned_interviewer_id": interviewer_a},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 409

    # update without changing slot should still work
    res = client.put(
        f"/interviews/{second_id}",
        json={"focus_tech_areas": ["Python", "SQL"]},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 200


def test_interviewer_availability_filter():
    """The interviewers list should hide whoever is booked in the given slot."""
    hr_token = get_hr_token()
    _, busy_id = get_interviewer_token_and_id()
    free_id = _insert_user("freeiv@nucleusteq.com", UserRole.INTERVIEWER)
    job_id = create_job(hr_token)
    candidate_id = create_candidate(hr_token, job_id)

    res = client.post("/interviews/", json={
        "candidate_id": candidate_id,
        "job_id": job_id,
        "interview_date": "2026-09-01T10:00:00",
        "interview_time": "10:00",
        "assigned_interviewer_id": busy_id,
        "focus_tech_areas": ["Python"],
    }, headers={"Authorization": f"Bearer {hr_token}"})
    assert res.status_code == 201

    # same slot -> busy interviewer hidden, free one still there
    res = client.get(
        "/users/interviewers?interview_date=2026-09-01T10:00:00&interview_time=10:00",
        headers={"Authorization": f"Bearer {hr_token}"},
    )
    assert res.status_code == 200
    ids = [u["id"] for u in res.json()]
    assert free_id in ids
    assert busy_id not in ids

    # different time same day -> everyone available
    res = client.get(
        "/users/interviewers?interview_date=2026-09-01T10:00:00&interview_time=14:00",
        headers={"Authorization": f"Bearer {hr_token}"},
    )
    ids = [u["id"] for u in res.json()]
    assert busy_id in ids

    # no slot given -> plain full list
    res = client.get("/users/interviewers", headers={"Authorization": f"Bearer {hr_token}"})
    ids = [u["id"] for u in res.json()]
    assert busy_id in ids and free_id in ids
