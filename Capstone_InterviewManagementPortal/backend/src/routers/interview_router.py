from fastapi import APIRouter, Depends, HTTPException, Query
from src.schemas.request.interview_request import ScheduleInterviewRequest, UpdateInterviewRequest
from src.schemas.response.interview_response import InterviewResponse, InterviewListResponse
from src.services.interview_service import InterviewService
from src.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/interviews", tags=["Interviews"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.post("/", response_model=InterviewResponse, status_code=201)
async def schedule_interview(
    request: ScheduleInterviewRequest,
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Only HR or Admin can schedule interviews")
    try:
        return InterviewService.schedule_interview(request.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=InterviewListResponse)
async def list_interviews(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    
    interviewer_id = None
    if current_user.get("role") == "interviewer":
        interviewer_id = current_user.get("sub")  
    return InterviewService.get_interviews(page, per_page, interviewer_id)

@router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        interview = InterviewService.get_interview_by_id(interview_id)
        
        if current_user.get("role") == "interviewer" and interview["assigned_interviewer_id"] != current_user.get("sub"):
            raise HTTPException(status_code=403, detail=" Not assigned to this interview")
        return interview
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: str,
    request: UpdateInterviewRequest,
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Only HR or Admin can update interviews")
    try:
        update_data = request.dict(exclude_unset=True)
        return InterviewService.update_interview(interview_id, update_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))