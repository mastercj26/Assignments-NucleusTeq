from src.core.database import Database
from src.exceptions.custom_exceptions import DuplicateException, NotFoundException
from src.constants.user_constants import EMAIL_ALREADY_EXISTS, USER_NOT_FOUND
from bson import ObjectId

class UserRepository:
    collection = Database.get_collection("users")

    @staticmethod
    def create_user(user_data: dict):
        existing = UserRepository.collection.find_one({"email": user_data["email"]})
        if existing:
            raise DuplicateException(EMAIL_ALREADY_EXISTS)
        result = UserRepository.collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return user_data

    @staticmethod
    def get_user_by_email(email: str):
        user = UserRepository.collection.find_one({"email": email})
        if not user:
            raise NotFoundException(USER_NOT_FOUND)
        user["_id"] = str(user["_id"])
        return user

    @staticmethod
    def get_user_by_id(user_id: str):
        user = UserRepository.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise NotFoundException(USER_NOT_FOUND)
        user["_id"] = str(user["_id"])
        return user

    @staticmethod
    def update_user(user_id: str, update_data: dict):
        result = UserRepository.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise NotFoundException(USER_NOT_FOUND)
        return UserRepository.get_user_by_id(user_id)
