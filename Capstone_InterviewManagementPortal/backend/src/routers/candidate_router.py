from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import io

from src.schemas.request.candidate_request import (
    CreateCandidateRequest,
    UpdateCandidateRequest,
    StatusUpdateRequest
)
from src.schemas.response.candidate_response import (
    CandidateResponse,
    CandidateListResponse,
    CandidateStatusHistoryResponse   # <-- IMPORT ADDED
)
from src.services.candidate_service import CandidateService
from src.exceptions.custom_exceptions import AppException
from src.core.security import decode_access_token

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

@router.post("/{candidate_id}/resume", status_code=200)
async def upload_resume(
    candidate_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    check_candidate_permission(current_user)
    try:
        contents = await file.read()
        result = CandidateService.upload_resume(candidate_id, contents, file.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{candidate_id}/resume")
async def download_resume(
    candidate_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        file = CandidateService.get_resume(candidate_id)
        response = StreamingResponse(io.BytesIO(file.read()), media_type=file.content_type)
        response.headers["Content-Disposition"] = f"attachment; filename={file.filename}"
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{candidate_id}/status")
async def update_candidate_status(
    candidate_id: str,
    request: StatusUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    check_candidate_permission(current_user)
    try:
        changed_by = current_user.get("sub") or current_user.get("email")
        result = CandidateService.update_candidate_status(
            candidate_id, request.status, changed_by, request.notes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{candidate_id}/status-history", response_model=CandidateStatusHistoryResponse)
async def get_status_history(
    candidate_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        history = CandidateService.get_candidate_status_history(candidate_id)
        return {"candidate_id": candidate_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))