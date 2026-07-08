from src.core.database import Database
from src.core.security import hash_password

db = Database.connect()
users = db["users"]

# Delete the existing admin if any
users.delete_one({"email": "admin@nucleusteq.com"})

# Create new admin with correct hash
admin = {
    "email": "admin@nucleusteq.com",
    "password": hash_password("admin123"),
    "role": "admin",
    "status": "active",
    "is_first_login": False,
    "first_name": "Admin",
    "last_name": "User"
}
users.insert_one(admin)
print("✅ Admin user created with correct password hash!")