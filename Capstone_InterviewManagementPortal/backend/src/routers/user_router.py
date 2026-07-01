from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from src.schemas.request.user_request import CreateUserRequest, UpdateUserRequest
from src.schemas.response.user_response import UserResponse, UserListResponse
from src.services.user_service import UserService
from src.exceptions.custom_exceptions import AppException
from src.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

# ---- CREATE (already exists) ----
@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    request: CreateUserRequest,
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can create users")
    try:
        user_data = request.dict()
        created = UserService.create_user(user_data)
        return created
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

# ---- LIST USERS ----
@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can list users")
    return UserService.get_all_users(page, per_page)

# ---- GET SINGLE USER ----
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can view user details")
    try:
        return UserService.get_user_by_id(user_id)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

# ---- UPDATE USER ----
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can update users")
    try:
        update_data = request.dict(exclude_unset=True)
        return UserService.update_user(user_id, update_data)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

# ---- DISABLE/ENABLE USER ----
@router.patch("/{user_id}/disable")
async def toggle_user_status(
    user_id: str,
    active: bool = Query(..., description="Set true to enable, false to disable"),
    current_user: dict = Depends(get_current_user)
):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can disable users")
    try:
        updated = UserService.disable_user(user_id, active)
        return {"message": f"User {'enabled' if active else 'disabled'} successfully", "user": updated}
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)