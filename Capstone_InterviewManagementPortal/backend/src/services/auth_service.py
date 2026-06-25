from src.repositories.user_repository import UserRepository
from src.core.security import verify_password, hash_password, create_access_token
from src.exceptions.custom_exceptions import UnauthorizedException
from src.constants.user_constants import INVALID_CREDENTIALS, FIRST_LOGIN_REQUIRED, PASSWORD_RESET_SUCCESS
from src.enums.user_enums import UserStatus

class AuthService:

    @staticmethod
    def login(email: str, password: str):
        user = UserRepository.get_user_by_email(email)
        if not verify_password(password, user["password"]):
            raise UnauthorizedException(INVALID_CREDENTIALS)
        
        if user.get("is_first_login", False):
            raise UnauthorizedException(FIRST_LOGIN_REQUIRED)
        
        token_data = {"sub": user["email"], "role": user["role"]}
        access_token = create_access_token(token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user["_id"],
            "email": user["email"],
            "role": user["role"]
        }

    @staticmethod
    def reset_password(email: str, old_password: str, new_password: str):
        user = UserRepository.get_user_by_email(email)
        if not verify_password(old_password, user["password"]):
            raise UnauthorizedException(INVALID_CREDENTIALS)
        
        hashed_new = hash_password(new_password)
        updated_user = UserRepository.update_user(
            user["_id"],
            {"password": hashed_new, "is_first_login": False, "status": UserStatus.ACTIVE}
        )
        return {"message": PASSWORD_RESET_SUCCESS}
