from pydantic import BaseModel, EmailStr, Field, validator
import re

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=12)

    @validator('email')
    def validate_nucleusteq_domain(cls, v):
        if not v.endswith('@nucleusteq.com'):
            raise ValueError('Email must be from nucleusteq.com domain')
        return v

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    old_password: str = Field(..., min_length=6, max_length=12)
    new_password: str = Field(..., min_length=6, max_length=12)

    @validator('email')
    def validate_nucleusteq_domain(cls, v):
        if not v.endswith('@nucleusteq.com'):
            raise ValueError('Email must be from nucleusteq.com domain')
        return v

    @validator('new_password')
    def validate_password_strength(cls, v):
        if not re.match(r'^[A-Za-z0-9@#$%^&+=!]{6,12}$', v):
            raise ValueError('Password must be 6-12 chars and contain alphanumeric or special characters')
        return v