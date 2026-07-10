from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse
import io

from src.schemas.request.candidate_request import (
    CreateCandidateRequest,
    UpdateCandidateRequest,
    StatusUpdateRequest
)
from src.schemas.response.candidate_response import (
    CandidateResponse,
    CandidateListResponse,
    CandidateStatusHistoryResponse
)
from src.services.candidate_service import CandidateService
from src.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/candidates", tags=["Candidates"])

# ---- Public (authenticated only) endpoints ----
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
    return CandidateService.get_candidate_by_id(candidate_id)

@router.get("/{candidate_id}/resume")
async def download_resume(
    candidate_id: str,
    current_user: dict = Depends(get_current_user)
):
    file = CandidateService.get_resume(candidate_id)
    response = StreamingResponse(io.BytesIO(file.read()), media_type=file.content_type)
    response.headers["Content-Disposition"] = f"attachment; filename={file.filename}"
    return response

@router.get("/{candidate_id}/status-history", response_model=CandidateStatusHistoryResponse)
async def get_status_history(
    candidate_id: str,
    current_user: dict = Depends(get_current_user)
):
    history = CandidateService.get_candidate_status_history(candidate_id)
    return {"candidate_id": candidate_id, "history": history}

# ---- Admin/HR only endpoints ----
@router.post("/", response_model=CandidateResponse, status_code=201)
async def create_candidate(
    request: CreateCandidateRequest,
    current_user: dict = Depends(require_role(["admin", "hr"]))
):
    return CandidateService.create_candidate(request.dict())

@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: str,
    request: UpdateCandidateRequest,
    current_user: dict = Depends(require_role(["admin", "hr"]))
):
    update_data = request.dict(exclude_unset=True)
    return CandidateService.update_candidate(candidate_id, update_data)

@router.post("/{candidate_id}/resume", status_code=200)
async def upload_resume(
    candidate_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(require_role(["admin", "hr"]))
):
    contents = await file.read()
    return CandidateService.upload_resume(candidate_id, contents, file.filename)

@router.patch("/{candidate_id}/status")
async def update_candidate_status(
    candidate_id: str,
    request: StatusUpdateRequest,
    current_user: dict = Depends(require_role(["admin", "hr"]))
):
    changed_by = current_user.get("sub") or current_user.get("email")
    return CandidateService.update_candidate_status(
        candidate_id, request.status, changed_by, request.notes
    )