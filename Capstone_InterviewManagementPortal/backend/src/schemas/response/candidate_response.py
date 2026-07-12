from pydantic import BaseModel
from typing import List, Optional
from src.enums.candidate_enums import CandidateStatus


class CandidateResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    mobile_number: str
    current_company: Optional[str]
    total_experience: float
    applied_job_id: str
    status: CandidateStatus
    resume_file_id: Optional[str] = None
    created_at: str
    updated_at: str


class CandidateListResponse(BaseModel):
    candidates: List[CandidateResponse]
    total: int
    page: int
    per_page: int
    pages: int


class StatusHistoryItem(BaseModel):
    status: CandidateStatus
    changed_at: str
    changed_by: str
    notes: Optional[str] = None


class CandidateStatusHistoryResponse(BaseModel):
    candidate_id: str
    history: List[StatusHistoryItem]


# Force rebuild to resolve any forward references
CandidateStatusHistoryResponse.model_rebuild()
