from pydantic import BaseModel
from typing import Optional
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
    resume_url: Optional[str]
    created_at: str
    updated_at: str

class CandidateListResponse(BaseModel):
    candidates: list[CandidateResponse]
    total: int
    page: int
    per_page: int
    pages: int