from src.core.database import Database
from src.exceptions.custom_exceptions import NotFoundException
from bson import ObjectId
from datetime import datetime

class InterviewRepository:
    collection = Database.get_collection("interviews")

    @staticmethod
    def _normalize(interview):
        if not interview:
            return None
        interview_copy = interview.copy()
        interview_copy["id"] = str(interview_copy.pop("_id"))
        return interview_copy

    @staticmethod
    def create(interview_data: dict):
        interview_data["created_at"] = datetime.utcnow().isoformat()
        interview_data["updated_at"] = datetime.utcnow().isoformat()
        result = InterviewRepository.collection.insert_one(interview_data)
        interview_data["_id"] = result.inserted_id
        return InterviewRepository._normalize(interview_data)

    @staticmethod
    def get_by_id(interview_id: str):
        interview = InterviewRepository.collection.find_one({"_id": ObjectId(interview_id)})
        if not interview:
            raise NotFoundException("Interview not found")
        return InterviewRepository._normalize(interview)

    @staticmethod
    def get_all(skip: int = 0, limit: int = 10, filter_by: dict = None):
        query = filter_by or {}
        interviews = InterviewRepository.collection.find(query).skip(skip).limit(limit)
        return [InterviewRepository._normalize(i) for i in interviews]

    @staticmethod
    def count(filter_by: dict = None):
        query = filter_by or {}
        return InterviewRepository.collection.count_documents(query)

    @staticmethod
    def update(interview_id: str, update_data: dict):
        update_data["updated_at"] = datetime.utcnow().isoformat()
        result = InterviewRepository.collection.update_one(
            {"_id": ObjectId(interview_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise NotFoundException("Interview not found")
        return InterviewRepository.get_by_id(interview_id)