from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    HR = "hr"
    INTERVIEWER = "interviewer"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FIRST_LOGIN = "first_login"