from fastapi import APIRouter, Depends, HTTPException
from src.services.dashboard_service import DashboardService
from src.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.get("/hr")
async def hr_dashboard(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") not in ["admin", "hr"]:
        raise HTTPException(status_code=403, detail="Only HR or Admin can view HR dashboard")
    return DashboardService.get_hr_dashboard()

@router.get("/interviewer")
async def interviewer_dashboard(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "interviewer":
        raise HTTPException(status_code=403, detail="Only Interviewer can view interviewer dashboard")
    return DashboardService.get_interviewer_dashboard(current_user.get("sub"))