from pydantic import BaseModel, EmailStr, Field, validator
from src.enums.user_enums import UserRole
import re

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=12)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: UserRole  # Must be one of "admin", "hr", "interviewer"

    @validator('email')
    def validate_nucleusteq_domain(cls, v):
        if not v.endswith('@nucleusteq.com'):
            raise ValueError('Email must be from nucleusteq.com domain')
        return v

    @validator('password')
    def validate_password_strength(cls, v):
        if not re.match(r'^[A-Za-z0-9@#$%^&+=!]{6,12}$', v):
            raise ValueError('Password must be 6-12 chars and contain alphanumeric or special characters')
        return v