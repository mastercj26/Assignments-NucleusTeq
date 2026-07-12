from src.core.database import Database
from src.exceptions.custom_exceptions import NotFoundException
from datetime import datetime, timezone


class FeedbackRepository:
    collection = Database.get_collection("feedbacks")

    @staticmethod
    def _normalize(feedback: dict) -> dict:
        if not feedback:
            return None
        feedback = feedback.copy()
        feedback["id"] = str(feedback.pop("_id"))
        return feedback

    @staticmethod
    def create(data: dict) -> dict:
        data["submitted_at"] = datetime.now(timezone.utc).isoformat()
        result = FeedbackRepository.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return FeedbackRepository._normalize(data)

    @staticmethod
    def get_by_interview_id(interview_id: str) -> dict:
        feedback = FeedbackRepository.collection.find_one({"interview_id": interview_id})
        if not feedback:
            raise NotFoundException("Feedback not found for this interview")
        return FeedbackRepository._normalize(feedback)

    @staticmethod
    def exists_for_interview(interview_id: str) -> bool:
        return FeedbackRepository.collection.find_one({"interview_id": interview_id}) is not None

    @staticmethod
    def get_by_interviewer(interviewer_id: str) -> list:
        cursor = FeedbackRepository.collection.find({"interviewer_id": interviewer_id})
        return [FeedbackRepository._normalize(f) for f in cursor]
