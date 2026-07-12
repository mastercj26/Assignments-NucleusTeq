from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from src.enums.candidate_enums import CandidateStatus
from src.utils.common import normalize_email
import re


class CreateCandidateRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    mobile_number: str = Field(..., min_length=10, max_length=10)
    current_company: Optional[str] = None
    total_experience: float = Field(..., ge=0, le=50)
    applied_job_id: str

    @field_validator("email")
    @classmethod
    def nucleusteq_domain(cls, v: str) -> str:
        v = normalize_email(v)
        if not re.match(r"^[a-z0-9._]+@nucleusteq\.com$", v):
            raise ValueError("Email can only contain letters, digits, dot or underscore and must be from nucleusteq.com domain")
        return v


    @field_validator("first_name", "last_name")
    @classmethod
    def name_letters_only(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not re.match(r"^[A-Za-z ]+$", v):
            raise ValueError("Name can only contain letters and spaces")
        return v

    @field_validator("mobile_number")
    @classmethod
    def digits_only(cls, v: str) -> str:
        if not re.match(r"^\d{10}$", v):
            raise ValueError("Mobile number must be exactly 10 digits")
        return v


class UpdateCandidateRequest(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = Field(None, min_length=10, max_length=10)
    current_company: Optional[str] = None
    total_experience: Optional[float] = Field(None, ge=0, le=50)
    applied_job_id: Optional[str] = None

    @field_validator("email")
    @classmethod
    def nucleusteq_domain(cls, v):
        if v is None:
            return v
        v = normalize_email(v)
        if not re.match(r"^[a-z0-9._]+@nucleusteq\.com$", v):
            raise ValueError("Email can only contain letters, digits, dot or underscore and must be from nucleusteq.com domain")
        return v


    @field_validator("first_name", "last_name")
    @classmethod
    def name_letters_only(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not re.match(r"^[A-Za-z ]+$", v):
            raise ValueError("Name can only contain letters and spaces")
        return v

    @field_validator("mobile_number")
    @classmethod
    def digits_only(cls, v: str) -> str:
        if v and not re.match(r"^\d{10}$", v):
            raise ValueError("Mobile number must be exactly 10 digits")
        return v


class StatusUpdateRequest(BaseModel):
    status: CandidateStatus
    notes: Optional[str] = None
