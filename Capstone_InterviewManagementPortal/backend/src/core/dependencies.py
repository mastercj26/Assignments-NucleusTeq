from fastapi import Depends, File, Request, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.security import decode_access_token
from src.enums.user_enums import UserRole
from src.exceptions.custom_exceptions import (
    ForbiddenException,
    UnauthorizedException,
    ValidationException,
)
from src.utils.common import RESUME_MAX_SIZE, RESUME_MIN_SIZE

_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(_bearer)
) -> dict:
    # middleware already decoded the token, HTTPBearer is kept for swagger
    user = getattr(request.state, "user", None)
    if user is not None:
        return user
    if credentials is None:
        raise UnauthorizedException("Not authenticated")
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise UnauthorizedException("Invalid or expired token")
    return payload


def require_role(required_roles: list[UserRole]):
    def checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user.get("role") not in required_roles:
            allowed = ", ".join(role.value for role in required_roles)
            raise ForbiddenException(f"Access denied. Required roles: {allowed}")
        return current_user

    return checker


async def get_validated_resume(file: UploadFile = File(...)) -> tuple[bytes, str]:
    """Validates the uploaded resume and returns (content, filename)."""
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise ValidationException("Only PDF files are allowed")

    content = await file.read()
    if not content:
        raise ValidationException("Uploaded file is empty")
    if len(content) < RESUME_MIN_SIZE:
        raise ValidationException("Uploaded file is too small to be a valid resume")
    if len(content) > RESUME_MAX_SIZE:
        raise ValidationException("File size exceeds the 10MB limit")
    if not content.startswith(b"%PDF"):
        raise ValidationException("File does not appear to be a valid PDF")

    return content, filename
