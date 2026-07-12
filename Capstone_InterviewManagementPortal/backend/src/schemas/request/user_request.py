from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from src.enums.user_enums import UserRole, UserStatus
from src.utils.common import normalize_email
import re


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: Optional[str] = Field(None, min_length=6, max_length=12)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: UserRole

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

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if v is not None and not re.match(r"^[A-Za-z0-9@#$%^&+=!]{6,12}$", v):
            raise ValueError("Password must be 6-12 chars: letters, digits, or @#$%^&+=!")
        return v


class UpdateUserRequest(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None

    @field_validator("first_name", "last_name")
    @classmethod
    def name_letters_only(cls, v):
        if v is None:
            return v
        v = v.strip()
        if not re.match(r"^[A-Za-z ]+$", v):
            raise ValueError("Name can only contain letters and spaces")
        return v

