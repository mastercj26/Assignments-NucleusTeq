from pydantic import BaseModel, Field, validator
from src.enums.interview_enums import Recommendation
from typing import List, Optional

class SubmitFeedbackRequest(BaseModel):
    technical_rating: int = Field(..., ge=1, le=5)
    communication_rating: int = Field(..., ge=1, le=5)
    problem_solving_rating: int = Field(..., ge=1, le=5)
    tech_areas_covered: List[str] = Field(..., min_length=1)
    comments: Optional[str] = None
    recommendation: Recommendation

    @validator('technical_rating', 'communication_rating', 'problem_solving_rating')
    def validate_ratings(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return v