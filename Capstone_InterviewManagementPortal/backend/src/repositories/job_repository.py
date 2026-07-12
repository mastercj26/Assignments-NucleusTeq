from src.core.database import Database
from src.exceptions.custom_exceptions import NotFoundException
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone


class JobRepository:
    collection = Database.get_collection("job_descriptions")

    @staticmethod
    def _to_object_id(id_str: str) -> ObjectId:
        try:
            return ObjectId(id_str)
        except (InvalidId, TypeError):
            raise NotFoundException("Job description not found")

    @staticmethod
    def _normalize(job: dict) -> dict:
        if not job:
            return None
        job = job.copy()
        job["id"] = str(job.pop("_id"))
        return job

    @staticmethod
    def create(data: dict) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        data["created_at"] = now
        data["updated_at"] = now
        result = JobRepository.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return JobRepository._normalize(data)

    @staticmethod
    def get_by_id(job_id: str) -> dict:
        doc = JobRepository.collection.find_one({"_id": JobRepository._to_object_id(job_id)})
        if not doc:
            raise NotFoundException("Job description not found")
        return JobRepository._normalize(doc)

    @staticmethod
    def get_all(skip: int = 0, limit: int = 10) -> list:
        cursor = JobRepository.collection.find().sort("_id", -1).skip(skip).limit(limit)  # newest first
        return [JobRepository._normalize(j) for j in cursor]

    @staticmethod
    def count() -> int:
        return JobRepository.collection.count_documents({})

    @staticmethod
    def update(job_id: str, data: dict) -> dict:
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = JobRepository.collection.update_one(
            {"_id": JobRepository._to_object_id(job_id)}, {"$set": data}
        )
        if result.matched_count == 0:
            raise NotFoundException("Job description not found")
        return JobRepository.get_by_id(job_id)
