from src.enums.candidate_enums import CandidateStatus
from src.enums.interview_enums import InterviewStatus, Recommendation
from src.exceptions.custom_exceptions import DuplicateException, ForbiddenException
from src.repositories.candidate_repository import CandidateRepository
from src.repositories.feedback_repository import FeedbackRepository
from src.repositories.interview_repository import InterviewRepository

class FeedbackService:

    @staticmethod
    def submit_feedback(data: dict, current_user_id: str, submitted_by: str) -> dict:
        interview = InterviewRepository.get_by_id(data["interview_id"])

        if interview["assigned_interviewer_id"] != current_user_id:
            raise ForbiddenException("You are not assigned to this interview")
        if FeedbackRepository.exists_for_interview(data["interview_id"]):
            raise DuplicateException("Feedback already submitted for this interview")

        data["interviewer_id"] = current_user_id
        feedback = FeedbackRepository.create(data)

        InterviewRepository.update(data["interview_id"], {"status": InterviewStatus.COMPLETED})

        recommendation = data.get("recommendation")
        if recommendation == Recommendation.SELECT:
            new_status = CandidateStatus.SELECTED
        elif recommendation == Recommendation.REJECT:
            new_status = CandidateStatus.REJECTED
        else:
            new_status = CandidateStatus.INTERVIEW_COMPLETED
        CandidateRepository.update(interview["candidate_id"], {"status": new_status})
        CandidateRepository.add_status_history(
            interview["candidate_id"],
            new_status,
            changed_by=submitted_by,
            notes=f"Feedback submitted with recommendation {data.get('recommendation')}",
        )
        return feedback

    @staticmethod
    def get_feedback_for_interview(interview_id: str) -> dict:
        return FeedbackRepository.get_by_interview_id(interview_id)
