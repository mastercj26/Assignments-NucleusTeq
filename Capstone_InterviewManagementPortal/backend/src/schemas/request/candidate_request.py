from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from src.enums.candidate_enums import CandidateStatus
import re

class CreateCandidateRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    mobile_number: str = Field(..., min_length=10, max_length=10)
    current_company: Optional[str] = None
    total_experience: float = Field(..., ge=0)
    applied_job_id: str  # reference to Job ID
    resume_url: Optional[str] = None  # will be handled later

    @validator('email')
    def validate_nucleusteq_domain(cls, v):
        if not v.endswith('@nucleusteq.com'):
            raise ValueError('Email must be from nucleusteq.com domain')
        return v

    @validator('mobile_number')
    def validate_mobile(cls, v):
        if not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Mobile number must be exactly 10 digits')
        return v

class UpdateCandidateRequest(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = Field(None, min_length=10, max_length=10)
    current_company: Optional[str] = None
    total_experience: Optional[float] = Field(None, ge=0)
    applied_job_id: Optional[str] = None
    status: Optional[CandidateStatus] = None

    @validator('email')
    def validate_nucleusteq_domain(cls, v):
        if v and not v.endswith('@nucleusteq.com'):
            raise ValueError('Email must be from nucleusteq.com domain')
        return v

    @validator('mobile_number')
    def validate_mobile(cls, v):
        if v and not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Mobile number must be exactly 10 digits')
        return v