from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from src.enums.candidate_enums import CandidateStatus
from src.enums.user_enums import UserRole
from src.exceptions.custom_exceptions import ForbiddenException, NotFoundException
from src.repositories.candidate_repository import CandidateRepository
from src.repositories.interview_repository import InterviewRepository


class CandidateService:

    @staticmethod
    def _assigned_candidate_ids(interviewer_id: str) -> list:
        return InterviewRepository.get_candidate_ids_for_interviewer(interviewer_id)

    @staticmethod
    def _check_interviewer_access(candidate_id: str, current_user: dict) -> None:
        # interviewers can only see candidates from their own interviews
        if current_user is None or current_user.get("role") != UserRole.INTERVIEWER:
            return
        assigned = CandidateService._assigned_candidate_ids(current_user.get("user_id"))
        if candidate_id not in assigned:
            raise ForbiddenException("You can only view candidates assigned to you")

    @staticmethod
    def create_candidate(data: dict, created_by: str = None) -> dict:
        data["status"] = CandidateStatus.PROFILE_CREATED
        data["status_history"] = [
            {
                "status": CandidateStatus.PROFILE_CREATED,
                "changed_at": datetime.now(timezone.utc).isoformat(),
                "changed_by": created_by,
                "notes": "Profile created",
            }
        ]
        return CandidateRepository.create(data)

    @staticmethod
    def get_all_candidates(page: int = 1, per_page: int = 10, current_user: dict = None) -> dict:
        skip = (page - 1) * per_page

        filter_by = None
        if current_user is not None and current_user.get("role") == UserRole.INTERVIEWER:
            ids = []
            for cid in CandidateService._assigned_candidate_ids(current_user.get("user_id")):
                try:
                    ids.append(ObjectId(cid))
                except (InvalidId, TypeError):
                    continue
            filter_by = {"_id": {"$in": ids}}

        candidates = CandidateRepository.get_all(skip=skip, limit=per_page, filter_by=filter_by)
        total = CandidateRepository.count(filter_by=filter_by)
        return {
            "candidates": candidates,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": max(1, (total + per_page - 1) // per_page),
        }

    @staticmethod
    def get_candidate_by_id(candidate_id: str, current_user: dict = None) -> dict:
        candidate = CandidateRepository.get_by_id(candidate_id)
        CandidateService._check_interviewer_access(candidate_id, current_user)
        return candidate

    @staticmethod
    def update_candidate(candidate_id: str, data: dict) -> dict:
        # status is updated through the status endpoint, not here
        data.pop("status", None)
        data.pop("status_history", None)
        return CandidateRepository.update(candidate_id, data)

    @staticmethod
    def update_candidate_status(
        candidate_id: str, status: CandidateStatus, changed_by: str, notes: str = None
    ) -> dict:
        updated = CandidateRepository.update(candidate_id, {"status": status})
        CandidateRepository.add_status_history(candidate_id, status, changed_by, notes)
        return updated

    @staticmethod
    def get_candidate_status_history(candidate_id: str, current_user: dict = None) -> list:
        CandidateService._check_interviewer_access(candidate_id, current_user)
        return CandidateRepository.get_status_history(candidate_id)

    @staticmethod
    def upload_resume(candidate_id: str, file_data: bytes, filename: str) -> dict:
        CandidateRepository.get_by_id(candidate_id)  # make sure candidate exists
        file_id = CandidateRepository.save_resume(candidate_id, file_data, filename)
        return {"file_id": file_id, "filename": filename}

    @staticmethod
    def get_resume(candidate_id: str, current_user: dict = None):
        CandidateService._check_interviewer_access(candidate_id, current_user)
        candidate = CandidateRepository.get_by_id(candidate_id)
        file_id = candidate.get("resume_file_id")
        if not file_id:
            raise NotFoundException("No resume uploaded for this candidate")
        return CandidateRepository.get_resume(file_id)
