from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from src.enums.interview_enums import InterviewStatus


class InterviewResponse(BaseModel):
    id: str
    candidate_id: str
    job_id: str
    interview_date: datetime
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    assigned_interviewer_id: str
    focus_tech_areas: List[str]
    status: InterviewStatus
    created_at: str
    updated_at: str


class InterviewListResponse(BaseModel):
    interviews: List[InterviewResponse]
    total: int
    page: int
    per_page: int
    pages: int
