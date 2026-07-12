from fastapi import APIRouter, Depends, Query

from src.core.dependencies import get_current_user, require_role
from src.enums.user_enums import UserRole
from src.schemas.request.job_request import CreateJobRequest, UpdateJobRequest
from src.schemas.response.job_response import JobListResponse, JobResponse
from src.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["Jobs"])

_hr_only = require_role([UserRole.HR])


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(body: CreateJobRequest, current_user: dict = Depends(_hr_only)):
    return JobService.create_job(body.model_dump())


@router.get("/", response_model=JobListResponse)
def list_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    return JobService.get_all_jobs(page, per_page)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str, current_user: dict = Depends(get_current_user)):
    return JobService.get_job_by_id(job_id)


@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: str, body: UpdateJobRequest, current_user: dict = Depends(_hr_only)):
    return JobService.update_job(job_id, body.model_dump(exclude_unset=True))
