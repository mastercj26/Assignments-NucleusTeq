from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from src.enums.interview_enums import InterviewStatus


class ScheduleInterviewRequest(BaseModel):
    candidate_id: str
    job_id: str
    interview_date: datetime
    interview_time: str
    assigned_interviewer_id: str
    focus_tech_areas: List[str] = Field(..., min_length=1)


class UpdateInterviewRequest(BaseModel):
    interview_date: Optional[datetime] = None
    interview_time: Optional[str] = None
    assigned_interviewer_id: Optional[str] = None
    focus_tech_areas: Optional[List[str]] = None
    status: Optional[InterviewStatus] = None
