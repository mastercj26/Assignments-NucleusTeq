from src.repositories.candidate_repository import CandidateRepository
from src.enums.candidate_enums import CandidateStatus
from src.exceptions.custom_exceptions import ValidationException
class CandidateService:
    
    @staticmethod
    def upload_resume(candidate_id: str, file_data: bytes, filename: str):
        """Upload resume file and update candidate."""
        if not filename.lower().endswith('.pdf'):
            raise ValidationException("Only PDF files are allowed")
        
        CandidateRepository.get_by_id(candidate_id)  
        file_id = CandidateRepository.save_resume(candidate_id, file_data, filename)
        return {"file_id": file_id, "filename": filename}

    @staticmethod
    def get_resume(candidate_id: str):
        """Retrieve resume file ID and return the file object."""
        candidate = CandidateRepository.get_by_id(candidate_id)
        if not candidate.get("resume_file_id"):
            raise NotFoundException("Resume not found for this candidate")
        file = CandidateRepository.get_resume(candidate["resume_file_id"])
        if not file:
            raise NotFoundException("Resume file not found")
        return file

    @staticmethod
    def update_candidate_status(candidate_id: str, new_status: str, changed_by: str, notes: str = None):
        """Update candidate status and add history entry."""
     
        candidate = CandidateRepository.get_by_id(candidate_id)
        current_status = candidate.get("status")
        if current_status == new_status:
            raise ValidationException("Status is already set to this value")
        # Update status in main document
        CandidateRepository.update(candidate_id, {"status": new_status})
        # Add history entry
        CandidateRepository.add_status_history(candidate_id, new_status, changed_by, notes)
        return {"message": "Status updated successfully", "new_status": new_status}

    @staticmethod
    def get_candidate_status_history(candidate_id: str):
        """Return status history for a candidate."""
        history = CandidateRepository.get_status_history(candidate_id)
        return history
    @staticmethod
    def create_candidate(candidate_data: dict):
        """Create a new candidate with default status."""
        candidate_data["status"] = CandidateStatus.PROFILE_CREATED
        return CandidateRepository.create(candidate_data)

    @staticmethod
    def get_all_candidates(page: int = 1, per_page: int = 10):
        """Get paginated list of candidates."""
        skip = (page - 1) * per_page
        candidates = CandidateRepository.get_all(skip=skip, limit=per_page)
        total = CandidateRepository.count()
        return {
            "candidates": candidates,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page
        }

    @staticmethod
    def get_candidate_by_id(candidate_id: str):
        """Get a single candidate by ID."""
        return CandidateRepository.get_by_id(candidate_id)

    @staticmethod
    def update_candidate(candidate_id: str, update_data: dict):
        """Update candidate fields."""
        return CandidateRepository.update(candidate_id, update_data)