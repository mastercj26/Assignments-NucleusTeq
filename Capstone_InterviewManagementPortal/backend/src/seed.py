from src.core.database import Database
from src.core.security import hash_password
from src.enums.user_enums import UserRole, UserStatus
from datetime import datetime, timezone


def seed_admin() -> None:
    db = Database.connect()
    users = db["users"]

    if users.find_one({"email": "admin@nucleusteq.com"}):
        print("Admin already exists, skipping.")
        return

    now = datetime.now(timezone.utc).isoformat()
    admin = {
        "email": "admin@nucleusteq.com",
        "password": hash_password("admin123"),
        "role": UserRole.ADMIN,
        "status": UserStatus.ACTIVE,
        "is_first_login": False,
        "first_name": "Admin",
        "last_name": "User",
        "created_at": now,
        "updated_at": now,
    }
    users.insert_one(admin)
    print("Admin created: admin@nucleusteq.com / admin123")


if __name__ == "__main__":
    seed_admin()
