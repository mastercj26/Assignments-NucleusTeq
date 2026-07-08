from src.repositories.feedback_repository import FeedbackRepository
from src.repositories.interview_repository import InterviewRepository
from src.repositories.candidate_repository import CandidateRepository
from src.enums.candidate_enums import CandidateStatus
from src.exceptions.custom_exceptions import ValidationException

class FeedbackService:

    @staticmethod
    def submit_feedback(feedback_data: dict, current_user_id: str):
       
        interview = InterviewRepository.get_by_id(feedback_data["interview_id"])
        if interview["assigned_interviewer_id"] != current_user_id:
            raise ValidationException("You are not assigned to this interview")
        
        try:
            existing = FeedbackRepository.get_by_interview_id(feedback_data["interview_id"])
            raise ValidationException("Feedback already submitted for this interview")
        except NotFoundException:
            pass
       
        feedback = FeedbackRepository.create(feedback_data)
     
        InterviewRepository.update(feedback_data["interview_id"], {"status": "completed"})
       
        recommendation = feedback_data.get("recommendation")
        if recommendation == "SELECT":
            CandidateRepository.update(interview["candidate_id"], {"status": CandidateStatus.SELECTED})
        elif recommendation == "REJECT":
            CandidateRepository.update(interview["candidate_id"], {"status": CandidateStatus.REJECTED})
        else: 
            CandidateRepository.update(interview["candidate_id"], {"status": CandidateStatus.INTERVIEW_COMPLETED})
        return feedback

    @staticmethod
    def get_feedback_for_interview(interview_id: str):
        return FeedbackRepository.get_by_interview_id(interview_id)