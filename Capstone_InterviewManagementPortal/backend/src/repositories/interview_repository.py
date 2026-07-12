from src.core.database import Database
from src.enums.interview_enums import InterviewStatus
from src.exceptions.custom_exceptions import NotFoundException
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timedelta, timezone


class InterviewRepository:
    collection = Database.get_collection("interviews")

    @staticmethod
    def _to_object_id(id_str: str) -> ObjectId:
        try:
            return ObjectId(id_str)
        except (InvalidId, TypeError):
            raise NotFoundException("Interview not found")

    @staticmethod
    def _normalize(interview: dict) -> dict:
        if not interview:
            return None
        interview = interview.copy()
        interview["id"] = str(interview.pop("_id"))
        return interview

    @staticmethod
    def create(data: dict) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        data["created_at"] = now
        data["updated_at"] = now
        result = InterviewRepository.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return InterviewRepository._normalize(data)

    @staticmethod
    def get_by_id(interview_id: str) -> dict:
        oid = InterviewRepository._to_object_id(interview_id)
        doc = InterviewRepository.collection.find_one({"_id": oid})
        if not doc:
            raise NotFoundException("Interview not found")
        return InterviewRepository._normalize(doc)

    @staticmethod
    def get_all(skip: int = 0, limit: int = 10, filter_by: dict = None) -> list:
        cursor = (
            InterviewRepository.collection.find(filter_by or {})
            .sort("_id", -1)
            .skip(skip)
            .limit(limit)
        )
        return [InterviewRepository._normalize(i) for i in cursor]

    @staticmethod
    def count(filter_by: dict = None) -> int:
        return InterviewRepository.collection.count_documents(filter_by or {})

    @staticmethod
    def update(interview_id: str, data: dict) -> dict:
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = InterviewRepository.collection.update_one(
            {"_id": InterviewRepository._to_object_id(interview_id)}, {"$set": data}
        )
        if result.matched_count == 0:
            raise NotFoundException("Interview not found")
        return InterviewRepository.get_by_id(interview_id)

    @staticmethod
    def has_conflict(
        interviewer_id: str,
        interview_date: datetime,
        interview_time: str,
        exclude_id: str = None,
    ) -> bool:
        # same interviewer, same day, same time slot
        day_start = interview_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        query = {
            "assigned_interviewer_id": interviewer_id,
            "interview_date": {"$gte": day_start, "$lt": day_end},
            "interview_time": interview_time.strip(),
            "status": InterviewStatus.SCHEDULED,
        }
        if exclude_id:
            query["_id"] = {"$ne": InterviewRepository._to_object_id(exclude_id)}
        return InterviewRepository.collection.find_one(query) is not None

    @staticmethod
    def get_candidate_ids_for_interviewer(interviewer_id: str) -> list:
        return InterviewRepository.collection.distinct(
            "candidate_id", {"assigned_interviewer_id": interviewer_id}
        )

    @staticmethod
    def get_busy_interviewer_ids(interview_date: datetime, interview_time: str) -> list:
        # interviewers having a scheduled interview on the same day + time
        day_start = interview_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        return InterviewRepository.collection.distinct(
            "assigned_interviewer_id",
            {
                "interview_date": {"$gte": day_start, "$lt": day_end},
                "interview_time": interview_time.strip(),
                "status": InterviewStatus.SCHEDULED,
            },
        )
