from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=12)

    @field_validator("email")
    @classmethod
    def nucleusteq_domain(cls, v: str) -> str:
        if not v.endswith("@nucleusteq.com"):
            raise ValueError("Email must be from nucleusteq.com domain")
        return v


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    old_password: str = Field(..., min_length=6, max_length=12)
    new_password: str = Field(..., min_length=6, max_length=12)

    @field_validator("email")
    @classmethod
    def nucleusteq_domain(cls, v: str) -> str:
        if not v.endswith("@nucleusteq.com"):
            raise ValueError("Email must be from nucleusteq.com domain")
        return v

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not re.match(r"^[A-Za-z0-9@#$%^&+=!]{6,12}$", v):
            raise ValueError("Password must be 6-12 chars: letters, digits, or @#$%^&+=!")
        return v
