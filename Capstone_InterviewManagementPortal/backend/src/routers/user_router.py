from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from src.core.dependencies import require_role
from src.enums.user_enums import UserRole
from src.schemas.request.user_request import CreateUserRequest, UpdateUserRequest
from src.schemas.response.user_response import (
    InterviewerOption,
    UserListResponse,
    UserResponse,
    UserStatusToggleResponse,
)
from src.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

_admin_only = require_role([UserRole.ADMIN])
_hr_only = require_role([UserRole.HR])


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(body: CreateUserRequest, current_user: dict = Depends(_admin_only)):
    return UserService.create_user(body.model_dump())


@router.get("/", response_model=UserListResponse)
def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(_admin_only),
):
    return UserService.get_all_users(page, per_page)


@router.get("/interviewers", response_model=list[InterviewerOption])
def list_interviewers(
    interview_date: Optional[datetime] = Query(None),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    current_user: dict = Depends(_hr_only),
):
    return UserService.list_interviewers(interview_date, start_time, end_time)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, current_user: dict = Depends(_admin_only)):
    return UserService.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, body: UpdateUserRequest, current_user: dict = Depends(_admin_only)):
    return UserService.update_user(user_id, body.model_dump(exclude_unset=True))


@router.patch("/{user_id}/disable", response_model=UserStatusToggleResponse)
def toggle_user_status(
    user_id: str,
    active: bool = Query(..., description="true to enable, false to disable"),
    current_user: dict = Depends(_admin_only),
):
    updated = UserService.toggle_user_status(user_id, active)
    return {
        "message": f"User {'enabled' if active else 'disabled'} successfully",
        "user": updated,
    }
