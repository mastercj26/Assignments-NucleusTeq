import io

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from src.core.dependencies import get_current_user, get_validated_resume, require_role
from src.enums.user_enums import UserRole
from src.schemas.request.candidate_request import (
    CreateCandidateRequest,
    StatusUpdateRequest,
    UpdateCandidateRequest,
)
from src.schemas.response.candidate_response import (
    CandidateListResponse,
    CandidateResponse,
    CandidateStatusHistoryResponse,
)
from src.schemas.response.common_response import ResumeUploadResponse
from src.services.candidate_service import CandidateService

router = APIRouter(prefix="/candidates", tags=["Candidates"])

_hr_only = require_role([UserRole.HR])
_hr_or_interviewer = require_role([UserRole.HR, UserRole.INTERVIEWER])


@router.post("/", response_model=CandidateResponse, status_code=201)
def create_candidate(body: CreateCandidateRequest, current_user: dict = Depends(_hr_only)):
    return CandidateService.create_candidate(body.model_dump(), created_by=current_user.get("sub"))


@router.get("/", response_model=CandidateListResponse)
def list_candidates(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    return CandidateService.get_all_candidates(page, per_page, current_user)


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: str, current_user: dict = Depends(get_current_user)):
    return CandidateService.get_candidate_by_id(candidate_id, current_user)


@router.put("/{candidate_id}", response_model=CandidateResponse)
def update_candidate(
    candidate_id: str,
    body: UpdateCandidateRequest,
    current_user: dict = Depends(_hr_only),
):
    return CandidateService.update_candidate(candidate_id, body.model_dump(exclude_unset=True))


@router.post("/{candidate_id}/resume", response_model=ResumeUploadResponse)
def upload_resume(
    candidate_id: str,
    resume: tuple[bytes, str] = Depends(get_validated_resume),
    current_user: dict = Depends(_hr_only),
):
    content, filename = resume
    return CandidateService.upload_resume(candidate_id, content, filename)


@router.get("/{candidate_id}/resume")
def download_resume(candidate_id: str, current_user: dict = Depends(_hr_or_interviewer)):
    file = CandidateService.get_resume(candidate_id, current_user)
    return StreamingResponse(
        io.BytesIO(file.read()),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={file.filename}"},
    )


@router.patch("/{candidate_id}/status", response_model=CandidateResponse)
def update_candidate_status(
    candidate_id: str,
    body: StatusUpdateRequest,
    current_user: dict = Depends(_hr_only),
):
    return CandidateService.update_candidate_status(
        candidate_id, body.status, changed_by=current_user.get("sub"), notes=body.notes
    )


@router.get("/{candidate_id}/status-history", response_model=CandidateStatusHistoryResponse)
def get_status_history(candidate_id: str, current_user: dict = Depends(get_current_user)):
    history = CandidateService.get_candidate_status_history(candidate_id, current_user)
    return {"candidate_id": candidate_id, "history": history}
