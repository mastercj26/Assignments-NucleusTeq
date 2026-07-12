from src.core.database import Database
from src.exceptions.custom_exceptions import DuplicateException, NotFoundException
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, timezone
from gridfs import GridFS


class CandidateRepository:
    collection = Database.get_collection("candidates")
    fs = GridFS(Database.connect())

    @staticmethod
    def _to_object_id(id_str: str) -> ObjectId:
        try:
            return ObjectId(id_str)
        except (InvalidId, TypeError):
            raise NotFoundException("Candidate not found")

    @staticmethod
    def _normalize(cand: dict) -> dict:
        if not cand:
            return None
        cand = cand.copy()
        cand["id"] = str(cand.pop("_id"))
        return cand

    @staticmethod
    def check_unique(email: str, mobile: str, exclude_id: str = None):
        email_query = {"email": email}
        if exclude_id:
            email_query["_id"] = {"$ne": ObjectId(exclude_id)}
        if CandidateRepository.collection.find_one(email_query):
            raise DuplicateException("Email already exists")

        mobile_query = {"mobile_number": mobile}
        if exclude_id:
            mobile_query["_id"] = {"$ne": ObjectId(exclude_id)}
        if CandidateRepository.collection.find_one(mobile_query):
            raise DuplicateException("Mobile number already exists")

    @staticmethod
    def create(data: dict) -> dict:
        CandidateRepository.check_unique(data["email"], data["mobile_number"])
        now = datetime.now(timezone.utc).isoformat()
        data["created_at"] = now
        data["updated_at"] = now
        result = CandidateRepository.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return CandidateRepository._normalize(data)

    @staticmethod
    def get_by_id(candidate_id: str) -> dict:
        oid = CandidateRepository._to_object_id(candidate_id)
        cand = CandidateRepository.collection.find_one({"_id": oid})
        if not cand:
            raise NotFoundException("Candidate not found")
        return CandidateRepository._normalize(cand)

    @staticmethod
    def get_all(skip: int = 0, limit: int = 10, filter_by: dict = None) -> list:
        cursor = (
            CandidateRepository.collection.find(filter_by or {})
            .sort("_id", -1)
            .skip(skip)
            .limit(limit)
        )
        return [CandidateRepository._normalize(c) for c in cursor]

    @staticmethod
    def count(filter_by: dict = None) -> int:
        return CandidateRepository.collection.count_documents(filter_by or {})

    @staticmethod
    def update(candidate_id: str, data: dict) -> dict:
        if "email" in data or "mobile_number" in data:
            current = CandidateRepository.collection.find_one(
                {"_id": CandidateRepository._to_object_id(candidate_id)}
            )
            if not current:
                raise NotFoundException("Candidate not found")
            email = data.get("email", current.get("email"))
            mobile = data.get("mobile_number", current.get("mobile_number"))
            CandidateRepository.check_unique(email, mobile, exclude_id=candidate_id)

        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = CandidateRepository.collection.update_one(
            {"_id": CandidateRepository._to_object_id(candidate_id)}, {"$set": data}
        )
        if result.matched_count == 0:
            raise NotFoundException("Candidate not found")
        return CandidateRepository.get_by_id(candidate_id)

    @staticmethod
    def save_resume(candidate_id: str, file_data: bytes, filename: str) -> str:
        file_id = CandidateRepository.fs.put(
            file_data, filename=filename, content_type="application/pdf", candidate_id=candidate_id
        )
        CandidateRepository.collection.update_one(
            {"_id": CandidateRepository._to_object_id(candidate_id)},
            {
                "$set": {
                    "resume_file_id": str(file_id),
                    "resume_filename": filename,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
            },
        )
        return str(file_id)

    @staticmethod
    def get_resume(file_id: str):
        try:
            return CandidateRepository.fs.get(ObjectId(file_id))
        except Exception:
            raise NotFoundException("Resume not found")

    @staticmethod
    def add_status_history(candidate_id: str, status: str, changed_by: str, notes: str = None):
        entry = {
            "status": status,
            "changed_at": datetime.now(timezone.utc).isoformat(),
            "changed_by": changed_by,
            "notes": notes,
        }
        CandidateRepository.collection.update_one(
            {"_id": CandidateRepository._to_object_id(candidate_id)},
            {
                "$push": {"status_history": entry},
                "$set": {"updated_at": datetime.now(timezone.utc).isoformat()},
            },
        )

    @staticmethod
    def get_status_history(candidate_id: str) -> list:
        doc = CandidateRepository.collection.find_one(
            {"_id": CandidateRepository._to_object_id(candidate_id)}, {"status_history": 1}
        )
        if not doc:
            raise NotFoundException("Candidate not found")
        return doc.get("status_history", [])
