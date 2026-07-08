from pydantic import BaseModel
from src.enums.interview_enums import Recommendation
from typing import List, Optional

class FeedbackResponse(BaseModel):
    id: str
    interview_id: str
    technical_rating: int
    communication_rating: int
    problem_solving_rating: int
    tech_areas_covered: List[str]
    comments: Optional[str]
    recommendation: Recommendation
    submitted_at: str