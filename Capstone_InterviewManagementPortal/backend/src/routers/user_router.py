from fastapi import APIRouter, Depends, HTTPException
from src.schemas.request.user_request import CreateUserRequest
from src.schemas.response.user_response import UserResponse
from src.services.user_service import UserService
from src.exceptions.custom_exceptions import AppException
from src.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBearer()

# Helper to get current user from token (will be used for authorization)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,
    current_user: dict = Depends(get_current_user)  # <-- Only authenticated users can create
):
    # Role-based check: only Admin can create users (optional, but required by spec)
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can create users")
    
    try:
        user_data = request.dict()
        created = UserService.create_user(user_data)
        return created
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)