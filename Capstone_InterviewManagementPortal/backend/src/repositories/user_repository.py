from src.core.database import Database
from src.exceptions.custom_exceptions import DuplicateException, NotFoundException
from src.constants.user_constants import EMAIL_ALREADY_EXISTS, USER_NOT_FOUND
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone


class UserRepository:
    collection = Database.get_collection("users")

    @staticmethod
    def _to_object_id(id_str: str) -> ObjectId:
        try:
            return ObjectId(id_str)
        except (InvalidId, TypeError):
            raise NotFoundException(USER_NOT_FOUND)

    @staticmethod
    def _normalize(user: dict) -> dict:
        if not user:
            return None
        user = user.copy()
        user["id"] = str(user.pop("_id"))
        user.pop("password", None)
        return user

    @staticmethod
    def create_user(data: dict) -> dict:
        if UserRepository.collection.find_one({"email": data["email"]}):
            raise DuplicateException(EMAIL_ALREADY_EXISTS)
        now = datetime.now(timezone.utc).isoformat()
        data["created_at"] = now
        data["updated_at"] = now
        result = UserRepository.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return UserRepository._normalize(data)

    @staticmethod
    def get_user_by_email(email: str) -> dict:
        user = UserRepository.collection.find_one({"email": email})
        if not user:
            raise NotFoundException(USER_NOT_FOUND)
        user["_id"] = str(user["_id"])
        return user

    @staticmethod
    def get_user_by_id(user_id: str) -> dict:
        user = UserRepository.collection.find_one({"_id": UserRepository._to_object_id(user_id)})
        if not user:
            raise NotFoundException(USER_NOT_FOUND)
        return UserRepository._normalize(user)

    @staticmethod
    def update_user(user_id: str, data: dict) -> dict:
        data.pop("password", None)
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = UserRepository.collection.update_one(
            {"_id": UserRepository._to_object_id(user_id)}, {"$set": data}
        )
        if result.matched_count == 0:
            raise NotFoundException(USER_NOT_FOUND)
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def update_password(user_id: str, hashed_password: str, extra_fields: dict = None):
        data = {"password": hashed_password, "updated_at": datetime.now(timezone.utc).isoformat()}
        if extra_fields:
            data.update(extra_fields)
        UserRepository.collection.update_one(
            {"_id": UserRepository._to_object_id(user_id)}, {"$set": data}
        )

    @staticmethod
    def get_all_users(skip: int = 0, limit: int = 10) -> list:
        cursor = UserRepository.collection.find().sort("_id", -1).skip(skip).limit(limit)  # newest first
        return [UserRepository._normalize(u) for u in cursor if u]

    @staticmethod
    def get_users_by_role(role: str) -> list:
        cursor = UserRepository.collection.find({"role": role})
        return [UserRepository._normalize(u) for u in cursor if u]

    @staticmethod
    def count_users() -> int:
        return UserRepository.collection.count_documents({})
