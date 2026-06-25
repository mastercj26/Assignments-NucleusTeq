from src.core.database import Database
from src.core.security import hash_password
from src.enums.user_enums import UserRole, UserStatus

def seed_admin():
    db = Database.connect()
    users = db["users"]
    
    if users.find_one({"email": "admin@nucleusteq.com"}):
        print("Admin user already exists!")
        return
    
    # Create admin user
    admin = {
        "email": "admin@nucleusteq.com",
        "password": hash_password("admin123"),
        "role": UserRole.ADMIN,
        "status": UserStatus.ACTIVE,
        "is_first_login": False,
        "first_name": "Admin",
        "last_name": "User"
    }
    users.insert_one(admin)
    print(" Admin user created successfully!")
    print("   Email: admin@nucleusteq.com")
    print("   Password: admin123")

if __name__ == "__main__":
    seed_admin()
