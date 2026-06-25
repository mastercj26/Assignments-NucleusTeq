from fastapi import APIRouter, HTTPException
from src.schemas.request.auth_request import LoginRequest, ResetPasswordRequest
from src.schemas.response.auth_response import TokenResponse
from src.services.auth_service import AuthService
from src.exceptions.custom_exceptions import AppException

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    try:
        result = AuthService.login(request.email, request.password)
        return result
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    try:
        result = AuthService.reset_password(
            request.email,
            request.old_password,
            request.new_password
        )
        return result
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)