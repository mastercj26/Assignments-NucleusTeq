from src.repositories.interview_repository import InterviewRepository
from src.repositories.user_repository import UserRepository
from src.core.security import hash_password
from src.enums.user_enums import UserRole, UserStatus
from src.constants.user_constants import DEFAULT_USER_PASSWORD
from src.exceptions.custom_exceptions import ValidationException


class UserService:

    @staticmethod
    def create_user(data: dict) -> dict:
        # default password is used when none is given, user has to reset it on first login
        raw_password = data.get("password") or DEFAULT_USER_PASSWORD
        data["password"] = hash_password(raw_password)
        data["status"] = UserStatus.FIRST_LOGIN
        data["is_first_login"] = True
        return UserRepository.create_user(data)

    @staticmethod
    def get_all_users(page: int = 1, per_page: int = 10) -> dict:
        skip = (page - 1) * per_page
        users = UserRepository.get_all_users(skip=skip, limit=per_page)
        total = UserRepository.count_users()
        return {
            "users": users,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": max(1, (total + per_page - 1) // per_page),
        }

    @staticmethod
    def list_interviewers(interview_date=None, start_time=None, end_time=None) -> list:
        # used by HR while scheduling, exposes only basic fields.
        # when a slot is given, interviewers already booked in it are left out.
        interviewers = UserRepository.get_users_by_role(UserRole.INTERVIEWER)

        busy_ids = []
        if interview_date is not None and start_time and end_time:
            busy_ids = InterviewRepository.get_busy_interviewer_ids(
                interview_date, start_time, end_time
            )

        return [
            {
                "id": u["id"],
                "first_name": u.get("first_name", ""),
                "last_name": u.get("last_name", ""),
                "email": u["email"],
            }
            for u in interviewers
            if u.get("status") != UserStatus.INACTIVE and u["id"] not in busy_ids
        ]

    @staticmethod
    def get_user_by_id(user_id: str) -> dict:
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def update_user(user_id: str, data: dict) -> dict:
        if "password" in data:
            raise ValidationException("Use reset-password endpoint for password changes")
        return UserRepository.update_user(user_id, data)

    @staticmethod
    def toggle_user_status(user_id: str, active: bool) -> dict:
        status = UserStatus.ACTIVE if active else UserStatus.INACTIVE
        return UserRepository.update_user(user_id, {"status": status})
