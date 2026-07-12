from pydantic import BaseModel, Field
from src.enums.interview_enums import Recommendation
from typing import List, Optional


class SubmitFeedbackRequest(BaseModel):
    interview_id: str
    technical_rating: int = Field(..., ge=1, le=5)
    communication_rating: int = Field(..., ge=1, le=5)
    problem_solving_rating: int = Field(..., ge=1, le=5)
    tech_areas_covered: List[str] = Field(..., min_length=1)
    comments: Optional[str] = None
    recommendation: Recommendation
