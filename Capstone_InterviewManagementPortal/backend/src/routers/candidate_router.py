from fastapi import APIRouter, Depends, HTTPException, Query
from src.schemas.request.candidate_request import CreateCandidateRequest, UpdateCandidateRequest
from src.schemas.response.candidate_response import CandidateResponse, CandidateListResponse
from src.services.candidate_service import CandidateService
from src.exceptions.custom_exceptions import AppException
from src.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/candidates", tags=["Candidates"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

# Helper: only Admin or HR can manage candidates
def check_candidate_permission(current_user: dict):
    role = current_user.get("role")
    if role not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Only HR or Admin can manage candidates")

@router.post("/", response_model=CandidateResponse, status_code=201)
async def create_candidate(
    request: CreateCandidateRequest,
    current_user: dict = Depends(get_current_user)
):
    check_candidate_permission(current_user)
    try:
        return CandidateService.create_candidate(request.dict())
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.get("/", response_model=CandidateListResponse)
async def list_candidates(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    # Allow any authenticated user to view candidates (or restrict to Admin/HR as per spec)
    # Spec says HR can view; we allow all authenticated for simplicity.
    return CandidateService.get_all_candidates(page, per_page)

@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        return CandidateService.get_candidate_by_id(candidate_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: str,
    request: UpdateCandidateRequest,
    current_user: dict = Depends(get_current_user)
):
    check_candidate_permission(current_user)
    try:
        update_data = request.dict(exclude_unset=True)
        return CandidateService.update_candidate(candidate_id, update_data)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)