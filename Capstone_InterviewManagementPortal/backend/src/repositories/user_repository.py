from src.core.database import Database
from src.exceptions.custom_exceptions import DuplicateException, NotFoundException
from src.constants.user_constants import EMAIL_ALREADY_EXISTS, USER_NOT_FOUND
from bson import ObjectId
from datetime import datetime

class UserRepository:
    collection = Database.get_collection("users")

    @staticmethod
    def _normalize_user(user):
        """Convert MongoDB doc to public schema (remove password, rename _id -> id, ensure created_at)."""
        if not user:
            return None
        # Work on a copy so we don't mutate the original
        user_copy = user.copy()
        user_copy["id"] = str(user_copy.pop("_id"))
        if "created_at" not in user_copy:
            user_copy["created_at"] = datetime.utcnow().isoformat()
        user_copy.pop("password", None)
        return user_copy

    @staticmethod
    def create_user(user_data: dict):
        existing = UserRepository.collection.find_one({"email": user_data["email"]})
        if existing:
            raise DuplicateException(EMAIL_ALREADY_EXISTS)
        user_data["created_at"] = datetime.utcnow().isoformat()
        user_data["updated_at"] = datetime.utcnow().isoformat()
        result = UserRepository.collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return UserRepository._normalize_user(user_data)

    @staticmethod
    def get_user_by_email(email: str):
        """Return raw user with password (for authentication)."""
        user = UserRepository.collection.find_one({"email": email})
        if not user:
            raise NotFoundException(USER_NOT_FOUND)
        # Convert _id to string but **keep** password
        user["_id"] = str(user["_id"])
        return user   # password is present

    @staticmethod
    def get_user_by_id(user_id: str):
        """Return public user (without password)."""
        user = UserRepository.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise NotFoundException(USER_NOT_FOUND)
        return UserRepository._normalize_user(user)

    @staticmethod
    def update_user(user_id: str, update_data: dict):
        """Update user and return public version."""
        # Remove password if accidentally included
        update_data.pop("password", None)
        update_data["updated_at"] = datetime.utcnow().isoformat()
        result = UserRepository.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise NotFoundException(USER_NOT_FOUND)
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def update_user_fields(user_id: str, update_data: dict):
        """Alias for update_user (partial updates)."""
        return UserRepository.update_user(user_id, update_data)

    @staticmethod
    def get_all_users(skip: int = 0, limit: int = 10):
        """Return list of public users (no passwords)."""
        users = UserRepository.collection.find().skip(skip).limit(limit)
        result = []
        for user in users:
            normalized = UserRepository._normalize_user(user)
            if normalized:
                result.append(normalized)
        return result

    @staticmethod
    def count_users():
        return UserRepository.collection.count_documents({})