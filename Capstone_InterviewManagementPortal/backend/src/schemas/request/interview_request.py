import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from src.enums.interview_enums import InterviewStatus

TIME_FORMAT = r"^([01]\d|2[0-3]):[0-5]\d$"  # 24h HH:MM


class ScheduleInterviewRequest(BaseModel):
    candidate_id: str
    job_id: str
    interview_date: datetime
    start_time: str
    end_time: str
    assigned_interviewer_id: str
    focus_tech_areas: List[str] = Field(..., min_length=1)

    @field_validator("start_time", "end_time")
    @classmethod
    def valid_time(cls, v):
        if not re.match(TIME_FORMAT, v):
            raise ValueError("Time must be in HH:MM format (24 hour)")
        return v

    @model_validator(mode="after")
    def end_after_start(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return self


class UpdateInterviewRequest(BaseModel):
    interview_date: Optional[datetime] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    assigned_interviewer_id: Optional[str] = None
    focus_tech_areas: Optional[List[str]] = None
    status: Optional[InterviewStatus] = None

    @field_validator("start_time", "end_time")
    @classmethod
    def valid_time(cls, v):
        if v is not None and not re.match(TIME_FORMAT, v):
            raise ValueError("Time must be in HH:MM format (24 hour)")
        return v

    @model_validator(mode="after")
    def end_after_start(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return self
