from fastapi import APIRouter, Depends

from src.core.dependencies import get_current_user
from src.schemas.request.feedback_request import SubmitFeedbackRequest
from src.schemas.response.feedback_response import FeedbackResponse
from src.services.feedback_service import FeedbackService

router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"])


@router.post("/", response_model=FeedbackResponse, status_code=201)
def submit_feedback(body: SubmitFeedbackRequest, current_user: dict = Depends(get_current_user)):
    return FeedbackService.submit_feedback(
        body.model_dump(),
        current_user_id=current_user.get("user_id"),
        submitted_by=current_user.get("sub"),
    )


@router.get("/interview/{interview_id}", response_model=FeedbackResponse)
def get_feedback_for_interview(interview_id: str, current_user: dict = Depends(get_current_user)):
    return FeedbackService.get_feedback_for_interview(interview_id)
