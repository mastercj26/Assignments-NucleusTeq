from src.enums.candidate_enums import CandidateStatus
from src.enums.interview_enums import InterviewStatus
from src.enums.user_enums import UserRole
from src.exceptions.custom_exceptions import (
    DuplicateException,
    ForbiddenException,
    ValidationException,
)
from src.repositories.candidate_repository import CandidateRepository
from src.repositories.interview_repository import InterviewRepository
from src.repositories.job_repository import JobRepository
from src.repositories.user_repository import UserRepository


class InterviewService:

    @staticmethod
    def _validate_interviewer(interviewer_id: str) -> dict:
        interviewer = UserRepository.get_user_by_id(interviewer_id)
        if interviewer.get("role") != UserRole.INTERVIEWER:
            raise ValidationException("Assigned user is not an interviewer")
        return interviewer

    @staticmethod
    def _ensure_slot_available(interviewer_id, interview_date, start_time, end_time, exclude_id=None):
        if InterviewRepository.has_conflict(
            interviewer_id, interview_date, start_time, end_time, exclude_id=exclude_id
        ):
            raise DuplicateException(
                "Interviewer already has an interview in this time range"
            )

    @staticmethod
    def schedule_interview(data: dict, scheduled_by: str) -> dict:
        CandidateRepository.get_by_id(data["candidate_id"])
        JobRepository.get_by_id(data["job_id"])
        InterviewService._validate_interviewer(data["assigned_interviewer_id"])
        InterviewService._ensure_slot_available(
            data["assigned_interviewer_id"],
            data["interview_date"],
            data["start_time"],
            data["end_time"],
        )

        data["status"] = InterviewStatus.SCHEDULED
        interview = InterviewRepository.create(data)

        CandidateRepository.update(
            data["candidate_id"], {"status": CandidateStatus.INTERVIEW_SCHEDULED}
        )
        CandidateRepository.add_status_history(
            data["candidate_id"],
            CandidateStatus.INTERVIEW_SCHEDULED,
            changed_by=scheduled_by,
            notes=f"Interview scheduled (id: {interview['id']})",
        )
        return interview

    @staticmethod
    def get_interviews(page: int = 1, per_page: int = 10, interviewer_id: str = None) -> dict:
        skip = (page - 1) * per_page
        filter_by = {"assigned_interviewer_id": interviewer_id} if interviewer_id else {}
        interviews = InterviewRepository.get_all(skip=skip, limit=per_page, filter_by=filter_by)
        total = InterviewRepository.count(filter_by=filter_by)
        return {
            "interviews": interviews,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": max(1, (total + per_page - 1) // per_page),
        }

    @staticmethod
    def get_interview_by_id(interview_id: str, current_user: dict = None) -> dict:
        interview = InterviewRepository.get_by_id(interview_id)
        # interviewer can only open his own interviews
        if (
            current_user is not None
            and current_user.get("role") == UserRole.INTERVIEWER
            and interview["assigned_interviewer_id"] != current_user.get("user_id")
        ):
            raise ForbiddenException("Not assigned to this interview")
        return interview

    @staticmethod
    def update_interview(interview_id: str, data: dict) -> dict:
        # check for double booking if interviewer/date/time is changing
        if {"assigned_interviewer_id", "interview_date", "start_time", "end_time"} & data.keys():
            existing = InterviewRepository.get_by_id(interview_id)
            interviewer_id = data.get(
                "assigned_interviewer_id", existing["assigned_interviewer_id"]
            )
            interview_date = data.get("interview_date", existing["interview_date"])
            start_time = data.get("start_time", existing.get("start_time"))
            end_time = data.get("end_time", existing.get("end_time"))
            if start_time and end_time and end_time <= start_time:
                raise ValidationException("End time must be after start time")

            if "assigned_interviewer_id" in data:
                InterviewService._validate_interviewer(interviewer_id)
            InterviewService._ensure_slot_available(
                interviewer_id, interview_date, start_time, end_time, exclude_id=interview_id
            )

        return InterviewRepository.update(interview_id, data)
