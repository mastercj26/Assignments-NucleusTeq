from fastapi import APIRouter, Depends, HTTPException, Query
from src.schemas.request.job_request import CreateJobRequest, UpdateJobRequest
from src.schemas.response.job_response import JobResponse, JobListResponse
from src.services.job_service import JobService
from src.exceptions.custom_exceptions import AppException
from src.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/jobs", tags=["Jobs"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

# Helper: only HR or Admin can manage jobs
def check_job_permission(current_user: dict):
    role = current_user.get("role")
    if role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Only HR or Admin can manage jobs")

@router.post("/", response_model=JobResponse, status_code=201)
async def create_job(
    request: CreateJobRequest,
    current_user: dict = Depends(get_current_user)
):
    check_job_permission(current_user)
    try:
        return JobService.create_job(request.dict())
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get("/", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    # Anyone authenticated can view jobs
    return JobService.get_all_jobs(page, per_page)

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        return JobService.get_job_by_id(job_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    request: UpdateJobRequest,
    current_user: dict = Depends(get_current_user)
):
    check_job_permission(current_user)
    try:
        update_data = request.dict(exclude_unset=True)
        return JobService.update_job(job_id, update_data)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)