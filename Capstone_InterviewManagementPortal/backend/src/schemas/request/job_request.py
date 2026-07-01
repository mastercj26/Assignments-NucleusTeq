from pydantic import BaseModel, Field
from typing import List, Optional
from src.enums.job_enums import EmploymentType, JobStatus

class CreateJobRequest(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=100)
    job_details: str = Field(..., min_length=1)
    job_role: str = Field(..., min_length=1, max_length=100)
    required_skills: List[str] = Field(..., min_items=1)
    experience_required: int = Field(..., ge=0)
    employment_type: EmploymentType
    location: str = Field(..., min_length=1, max_length=100)
    status: Optional[JobStatus] = JobStatus.OPEN

class UpdateJobRequest(BaseModel):
    job_title: Optional[str] = Field(None, min_length=1, max_length=100)
    job_details: Optional[str] = Field(None, min_length=1)
    job_role: Optional[str] = Field(None, min_length=1, max_length=100)
    required_skills: Optional[List[str]] = Field(None, min_items=1)
    experience_required: Optional[int] = Field(None, ge=0)
    employment_type: Optional[EmploymentType] = None
    location: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[JobStatus] = None