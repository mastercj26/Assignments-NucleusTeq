from src.repositories.user_repository import UserRepository
from src.core.security import hash_password
from src.enums.user_enums import UserStatus
from src.exceptions.custom_exceptions import ValidationException

class UserService:

    @staticmethod
    def create_user(user_data: dict):
        # Hash the password
        user_data["password"] = hash_password(user_data["password"])
        # Set default status and first login flag
        user_data["status"] = UserStatus.ACTIVE
        user_data["is_first_login"] = True
        # Insert using repository
        created_user = UserRepository.create_user(user_data)
        # Remove password from response
        created_user.pop("password", None)
        return created_user