from pydantic import BaseModel
from typing import List, Optional
from src.enums.job_enums import EmploymentType, JobStatus

class JobResponse(BaseModel):
    id: str
    job_title: str
    job_details: str
    job_role: str
    required_skills: List[str]
    experience_required: int
    employment_type: EmploymentType
    location: str
    status: JobStatus
    created_at: str
    updated_at: str

class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    per_page: int
    pages: int