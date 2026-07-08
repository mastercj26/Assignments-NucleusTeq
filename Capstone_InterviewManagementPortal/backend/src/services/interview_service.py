from src.repositories.interview_repository import InterviewRepository
from src.repositories.candidate_repository import CandidateRepository
from src.repositories.job_repository import JobRepository
from src.repositories.user_repository import UserRepository
from src.enums.candidate_enums import CandidateStatus

class InterviewService:

    @staticmethod
    def schedule_interview(interview_data: dict):
        
        CandidateRepository.get_by_id(interview_data["candidate_id"])
      
        JobRepository.get_by_id(interview_data["job_id"])
       
        UserRepository.get_by_id(interview_data["assigned_interviewer_id"])
       
        interview_data["status"] = "scheduled"
        created = InterviewRepository.create(interview_data)
        
        CandidateRepository.update(interview_data["candidate_id"], {"status": CandidateStatus.INTERVIEW_SCHEDULED})
        return created

    @staticmethod
    def get_interviews(page: int = 1, per_page: int = 10, interviewer_id: str = None):
        skip = (page - 1) * per_page
        filter_by = {}
        if interviewer_id:
            filter_by["assigned_interviewer_id"] = interviewer_id
        interviews = InterviewRepository.get_all(skip=skip, limit=per_page, filter_by=filter_by)
        total = InterviewRepository.count(filter_by=filter_by)
        return {
            "interviews": interviews,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page
        }

    @staticmethod
    def get_interview_by_id(interview_id: str):
        return InterviewRepository.get_by_id(interview_id)

    @staticmethod
    def update_interview(interview_id: str, update_data: dict):
       
        if "status" in update_data and update_data["status"] == "completed":
           
            pass
        return InterviewRepository.update(interview_id, update_data)