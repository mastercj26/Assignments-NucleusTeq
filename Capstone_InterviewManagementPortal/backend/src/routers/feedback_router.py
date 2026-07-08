from fastapi import APIRouter, Depends, HTTPException
from src.schemas.request.feedback_request import SubmitFeedbackRequest
from src.schemas.response.feedback_response import FeedbackResponse
from src.services.feedback_service import FeedbackService
from src.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.post("/", response_model=FeedbackResponse, status_code=201)
async def submit_feedback(
    request: SubmitFeedbackRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        return FeedbackService.submit_feedback(request.dict(), current_user.get("sub"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/interview/{interview_id}", response_model=FeedbackResponse)
async def get_feedback_for_interview(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        return FeedbackService.get_feedback_for_interview(interview_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))