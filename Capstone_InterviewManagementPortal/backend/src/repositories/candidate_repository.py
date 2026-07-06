from src.core.database import Database
from src.exceptions.custom_exceptions import DuplicateException, NotFoundException, ValidationException
from bson import ObjectId
from datetime import datetime

class CandidateRepository:
    collection = Database.get_collection("candidates")

    @staticmethod
    def _normalize_candidate(cand):
        if not cand:
            return None
        cand_copy = cand.copy()
        cand_copy["id"] = str(cand_copy.pop("_id"))
        return cand_copy

    @staticmethod
    def check_unique(email: str, mobile: str, exclude_id: str = None):
        # Check email uniqueness
        query = {"email": email}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        if CandidateRepository.collection.find_one(query):
            raise DuplicateException("Email already exists")

        # Check mobile uniqueness
        query = {"mobile_number": mobile}
        if exclude_id:
            query["_id"] = {"$ne": ObjectId(exclude_id)}
        if CandidateRepository.collection.find_one(query):
            raise DuplicateException("Mobile number already exists")

    @staticmethod
    def create(candidate_data: dict):
        # Validate uniqueness
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
        # If email or mobile is being updated, check uniqueness
        if "email" in update_data or "mobile_number" in update_data:
            email = update_data.get("email")
            mobile = update_data.get("mobile_number")
            # Get current candidate to know existing values
            current = CandidateRepository.collection.find_one({"_id": ObjectId(candidate_id)})
            if not current:
                raise NotFoundException("Candidate not found")
            email_to_check = email or current.get("email")
            mobile_to_check = mobile or current.get("mobile_number")
            CandidateRepository.check_unique(email_to_check, mobile_to_check, exclude_id=candidate_id)

        update_data["updated_at"] = datetime.utcnow().isoformat()
        result = CandidateRepository.collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise NotFoundException("Candidate not found")
        return CandidateRepository.get_by_id(candidate_id)