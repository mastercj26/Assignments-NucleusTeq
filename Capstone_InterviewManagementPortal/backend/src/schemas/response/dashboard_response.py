from pydantic import BaseModel


class HRDashboardResponse(BaseModel):
    total_jobs: int
    total_candidates: int
    scheduled_interviews: int
    selected_candidates: int
    rejected_candidates: int


class InterviewerDashboardResponse(BaseModel):
    assigned_interviews: int
    pending_feedback: int
    completed_feedback: int
