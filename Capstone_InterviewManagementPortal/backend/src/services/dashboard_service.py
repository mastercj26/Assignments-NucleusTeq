from src.repositories.job_repository import JobRepository
from src.repositories.candidate_repository import CandidateRepository
from src.repositories.interview_repository import InterviewRepository
from src.repositories.feedback_repository import FeedbackRepository
from src.enums.candidate_enums import CandidateStatus


class DashboardService:

    @staticmethod
    def get_hr_dashboard():
        total_jobs = JobRepository.count()
        total_candidates = CandidateRepository.count()
        scheduled_interviews = InterviewRepository.count(filter_by={"status": "scheduled"})
        selected = CandidateRepository.count(filter_by={"status": CandidateStatus.SELECTED})
        rejected = CandidateRepository.count(filter_by={"status": CandidateStatus.REJECTED})
        return {
            "total_jobs": total_jobs,
            "total_candidates": total_candidates,
            "scheduled_interviews": scheduled_interviews,
            "selected_candidates": selected,
            "rejected_candidates": rejected,
        }

    @staticmethod
    def get_interviewer_dashboard(interviewer_id: str):
        assigned = InterviewRepository.count(filter_by={"assigned_interviewer_id": interviewer_id})
        pending = InterviewRepository.count(
            filter_by={"assigned_interviewer_id": interviewer_id, "status": "scheduled"}
        )

        completed = InterviewRepository.count(
            filter_by={"assigned_interviewer_id": interviewer_id, "status": "completed"}
        )
        return {
            "assigned_interviews": assigned,
            "pending_feedback": pending,
            "completed_feedback": completed,
        }
