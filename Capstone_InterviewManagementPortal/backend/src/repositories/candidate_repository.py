from src.core.database import Database
from src.exceptions.custom_exceptions import DuplicateException, NotFoundException
from bson import ObjectId
from datetime import datetime
from gridfs import GridFS

class CandidateRepository:
    collection = Database.get_collection("candidates")
    fs = GridFS(Database.db)   # GridFS instance

    @staticmethod
    def _normalize_candidate(cand):
        if not cand:
            return None
        cand_copy = cand.copy()
        cand_copy["id"] = str(cand_copy.pop("_id"))
        return cand_copy

    @staticmethod
    def check_unique(email: str, mobile: str, exclude_id: str = None):
        query = {"email": email}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        if CandidateRepository.collection.find_one(query):
            raise DuplicateException("Email already exists")

        query = {"mobile_number": mobile}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        if CandidateRepository.collection.find_one(query):
            raise DuplicateException("Mobile number already exists")

    @staticmethod
    def create(candidate_data: dict):
        CandidateRepository.check_unique(
            candidate_data["email"],
            candidate_data["mobile_number"]
        )
        candidate_data["created_at"] = datetime.utcnow().isoformat()
        candidate_data["updated_at"] = datetime.utcnow().isoformat()
        result = CandidateRepository.collection.insert_one(candidate_data)
        candidate_data["_id"] = result.inserted_id
        return CandidateRepository._normalize_candidate(candidate_data)

    @staticmethod
    def get_by_id(candidate_id: str):
        cand = CandidateRepository.collection.find_one({"_id": ObjectId(candidate_id)})
        if not cand:
            raise NotFoundException("Candidate not found")
        return CandidateRepository._normalize_candidate(cand)

    @staticmethod
    def get_all(skip: int = 0, limit: int = 10):
        candidates = CandidateRepository.collection.find().skip(skip).limit(limit)
        return [CandidateRepository._normalize_candidate(c) for c in candidates]

    @staticmethod
    def count():
        return CandidateRepository.collection.count_documents({})

    @staticmethod
    def update(candidate_id: str, update_data: dict):
        if "email" in update_data or "mobile_number" in update_data:
            current = CandidateRepository.collection.find_one({"_id": ObjectId(candidate_id)})
            if not current:
                raise NotFoundException("Candidate not found")
            email = update_data.get("email", current.get("email"))
            mobile = update_data.get("mobile_number", current.get("mobile_number"))
            CandidateRepository.check_unique(email, mobile, exclude_id=candidate_id)

        update_data["updated_at"] = datetime.utcnow().isoformat()
        result = CandidateRepository.collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise NotFoundException("Candidate not found")
        return CandidateRepository.get_by_id(candidate_id)

    @staticmethod
    def save_resume(candidate_id: str, file_data: bytes, filename: str, content_type: str = "application/pdf"):
        file_id = CandidateRepository.fs.put(
            file_data,
            filename=filename,
            content_type=content_type,
            candidate_id=candidate_id
        )
        CandidateRepository.collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": {
                "resume_file_id": str(file_id),
                "resume_filename": filename,
                "updated_at": datetime.utcnow().isoformat()
            }}
        )
        return str(file_id)

    @staticmethod
    def get_resume(file_id: str):
        try:
            file = CandidateRepository.fs.get(ObjectId(file_id))
            return file
        except Exception:
            return None

    @staticmethod
    def add_status_history(candidate_id: str, status: str, changed_by: str, notes: str = None):
        entry = {
            "status": status,
            "changed_at": datetime.utcnow().isoformat(),
            "changed_by": changed_by,
            "notes": notes
        }
        CandidateRepository.collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$push": {"status_history": entry}, "$set": {"updated_at": datetime.utcnow().isoformat()}}
        )

    @staticmethod
    def get_status_history(candidate_id: str):
        candidate = CandidateRepository.collection.find_one(
            {"_id": ObjectId(candidate_id)},
            {"status_history": 1}
        )
        if not candidate:
            raise NotFoundException("Candidate not found")
        return candidate.get("status_history", [])