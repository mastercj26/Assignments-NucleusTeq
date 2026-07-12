from fastapi import APIRouter, Depends

from src.core.dependencies import require_role
from src.enums.user_enums import UserRole
from src.schemas.response.dashboard_response import (
    HRDashboardResponse,
    InterviewerDashboardResponse,
)
from src.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

_hr_admin = require_role([UserRole.ADMIN, UserRole.HR])
_interviewer = require_role([UserRole.INTERVIEWER])


@router.get("/hr", response_model=HRDashboardResponse)
def hr_dashboard(current_user: dict = Depends(_hr_admin)):
    return DashboardService.get_hr_dashboard()


@router.get("/interviewer", response_model=InterviewerDashboardResponse)
def interviewer_dashboard(current_user: dict = Depends(_interviewer)):
    return DashboardService.get_interviewer_dashboard(current_user.get("user_id"))
