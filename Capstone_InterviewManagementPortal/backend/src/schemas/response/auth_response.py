from pydantic import BaseModel
from typing import Optional
from src.enums.user_enums import UserRole, UserStatus

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: UserRole

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    status: UserStatus
    is_first_login: bool