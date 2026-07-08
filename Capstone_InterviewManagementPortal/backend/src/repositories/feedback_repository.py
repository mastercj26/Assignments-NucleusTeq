from src.core.database import Database
from src.exceptions.custom_exceptions import NotFoundException
from bson import ObjectId
from datetime import datetime

class FeedbackRepository:
    collection = Database.get_collection("feedbacks")

    @staticmethod
    def _normalize(feedback):
        if not feedback:
            return None
        feedback_copy = feedback.copy()
        feedback_copy["id"] = str(feedback_copy.pop("_id"))
        return feedback_copy

    @staticmethod
    def create(feedback_data: dict):
        feedback_data["submitted_at"] = datetime.utcnow().isoformat()
        result = FeedbackRepository.collection.insert_one(feedback_data)
        feedback_data["_id"] = result.inserted_id
        return FeedbackRepository._normalize(feedback_data)

    @staticmethod
    def get_by_interview_id(interview_id: str):
        feedback = FeedbackRepository.collection.find_one({"interview_id": interview_id})
        if not feedback:
            raise NotFoundException("Feedback not found for this interview")
        return FeedbackRepository._normalize(feedback)

    @staticmethod
    def get_by_interviewer(interviewer_id: str):
       
        pass