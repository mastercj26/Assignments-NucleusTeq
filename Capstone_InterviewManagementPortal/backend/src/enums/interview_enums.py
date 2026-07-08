from enum import Enum

class InterviewStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Recommendation(str, Enum):
    NEXT_ROUND = "NEXT_ROUND"
    SELECT = "SELECT"
    REJECT = "REJECT"