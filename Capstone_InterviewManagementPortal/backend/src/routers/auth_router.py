from fastapi import APIRouter, Depends

from src.core.dependencies import get_current_user
from src.schemas.request.auth_request import LoginRequest, ResetPasswordRequest
from src.schemas.response.auth_response import TokenResponse
from src.schemas.response.common_response import GenericMessageResponse
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    return AuthService.login(body.email, body.password)


@router.post("/reset-password", response_model=GenericMessageResponse)
def reset_password(body: ResetPasswordRequest):
    return AuthService.reset_password(body.email, body.old_password, body.new_password)


@router.post("/logout", response_model=GenericMessageResponse)
def logout(current_user: dict = Depends(get_current_user)):
    # JWT is stateless, client just discards the token
    return {"message": "Logged out successfully"}
