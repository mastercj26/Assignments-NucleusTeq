from src.repositories.candidate_repository import CandidateRepository
from src.enums.candidate_enums import CandidateStatus

class CandidateService:

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