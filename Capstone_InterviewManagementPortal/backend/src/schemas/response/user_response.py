from pydantic import BaseModel
from typing import List
from src.enums.user_enums import UserRole, UserStatus

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: UserRole
    status: UserStatus
    is_first_login: bool
    created_at: str

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    per_page: int
    pages: int