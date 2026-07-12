from src.constants.user_constants import (
    ACCOUNT_DISABLED,
    FIRST_LOGIN_REQUIRED,
    INVALID_CREDENTIALS,
    PASSWORD_RESET_SUCCESS,
)
from src.core.security import create_access_token, hash_password, verify_password
from src.enums.user_enums import UserStatus
from src.exceptions.custom_exceptions import ForbiddenException, UnauthorizedException
from src.repositories.user_repository import UserRepository
from src.utils.common import normalize_email


class AuthService:

    @staticmethod
    def login(email: str, password: str) -> dict:
        user = UserRepository.get_user_by_email(normalize_email(email))
        if not verify_password(password, user["password"]):
            raise UnauthorizedException(INVALID_CREDENTIALS)
        if user.get("status") == UserStatus.INACTIVE:
            raise ForbiddenException(ACCOUNT_DISABLED)
        if user.get("is_first_login", False):
            raise UnauthorizedException(FIRST_LOGIN_REQUIRED)

        token = create_access_token(
            {"sub": user["email"], "role": user["role"], "user_id": user["_id"]}
        )
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user["_id"],
            "email": user["email"],
            "role": user["role"],
        }

    @staticmethod
    def reset_password(email: str, old_password: str, new_password: str) -> dict:
        user = UserRepository.get_user_by_email(normalize_email(email))
        if not verify_password(old_password, user["password"]):
            raise UnauthorizedException(INVALID_CREDENTIALS)

        UserRepository.update_password(
            user["_id"],
            hash_password(new_password),
            extra_fields={"is_first_login": False, "status": UserStatus.ACTIVE},
        )
        return {"message": PASSWORD_RESET_SUCCESS}
