from fastapi import APIRouter, Depends, Query

from src.core.dependencies import get_current_user, require_role
from src.enums.user_enums import UserRole
from src.schemas.request.interview_request import (
    ScheduleInterviewRequest,
    UpdateInterviewRequest,
)
from src.schemas.response.interview_response import InterviewListResponse, InterviewResponse
from src.services.interview_service import InterviewService

router = APIRouter(prefix="/interviews", tags=["Interviews"])

_hr_only = require_role([UserRole.HR])


@router.post("/", response_model=InterviewResponse, status_code=201)
def schedule_interview(body: ScheduleInterviewRequest, current_user: dict = Depends(_hr_only)):
    return InterviewService.schedule_interview(
        body.model_dump(), scheduled_by=current_user.get("sub")
    )


@router.get("/", response_model=InterviewListResponse)
def list_interviews(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    # interviewers should only see their own interviews
    interviewer_id = None
    if current_user.get("role") == UserRole.INTERVIEWER:
        interviewer_id = current_user.get("user_id")
    return InterviewService.get_interviews(page, per_page, interviewer_id)


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(interview_id: str, current_user: dict = Depends(get_current_user)):
    return InterviewService.get_interview_by_id(interview_id, current_user)


@router.put("/{interview_id}", response_model=InterviewResponse)
def update_interview(
    interview_id: str,
    body: UpdateInterviewRequest,
    current_user: dict = Depends(_hr_only),
):
    return InterviewService.update_interview(interview_id, body.model_dump(exclude_unset=True))
