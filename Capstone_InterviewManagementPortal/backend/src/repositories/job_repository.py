from src.core.database import Database
from src.exceptions.custom_exceptions import NotFoundException, DuplicateException
from bson import ObjectId
from datetime import datetime

class JobRepository:
    collection = Database.get_collection("job_descriptions")

    @staticmethod
    def _normalize_job(job):
        if not job:
            return None
        job_copy = job.copy()
        job_copy["id"] = str(job_copy.pop("_id"))
        job_copy.pop("_id", None)  # just in case
        return job_copy

    @staticmethod
    def create(job_data: dict):
        job_data["created_at"] = datetime.utcnow().isoformat()
        job_data["updated_at"] = datetime.utcnow().isoformat()
        result = JobRepository.collection.insert_one(job_data)
        job_data["_id"] = result.inserted_id
        return JobRepository._normalize_job(job_data)

    @staticmethod
    def get_by_id(job_id: str):
        job = JobRepository.collection.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise NotFoundException("Job description not found")
        return JobRepository._normalize_job(job)

    @staticmethod
    def get_all(skip: int = 0, limit: int = 10):
        jobs = JobRepository.collection.find().skip(skip).limit(limit)
        return [JobRepository._normalize_job(job) for job in jobs]

    @staticmethod
    def count():
        return JobRepository.collection.count_documents({})

    @staticmethod
    def update(job_id: str, update_data: dict):
        update_data["updated_at"] = datetime.utcnow().isoformat()
        result = JobRepository.collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise NotFoundException("Job description not found")
        return JobRepository.get_by_id(job_id)