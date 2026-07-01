from src.repositories.user_repository import UserRepository
from src.core.security import hash_password
from src.enums.user_enums import UserStatus
from src.exceptions.custom_exceptions import ValidationException

class UserService:

    @staticmethod
    def create_user(user_data: dict):
        # Hash the password
        user_data["password"] = hash_password(user_data["password"])
        user_data["status"] = UserStatus.ACTIVE
        user_data["is_first_login"] = False
        created_user = UserRepository.create_user(user_data)
        # Remove password before returning (already removed by repository)
        return created_user

    @staticmethod
    def get_all_users(page: int = 1, per_page: int = 10):
        skip = (page - 1) * per_page
        users = UserRepository.get_all_users(skip=skip, limit=per_page)
        total = UserRepository.count_users()
        return {
            "users": users,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page
        }

    @staticmethod
    def get_user_by_id(user_id: str):
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def update_user(user_id: str, update_data: dict):
        # Prevent updating password via this endpoint
        if "password" in update_data:
            raise ValidationException("Use change-password endpoint for password updates")
        return UserRepository.update_user_fields(user_id, update_data)

    @staticmethod
    def disable_user(user_id: str, is_active: bool):
        status = UserStatus.ACTIVE if is_active else UserStatus.INACTIVE
        return UserRepository.update_user_fields(user_id, {"status": status})