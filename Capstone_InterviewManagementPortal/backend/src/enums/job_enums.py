from enum import Enum

class EmploymentType(str, Enum):
    FULL_TIME = "Full Time"
    INTERNSHIP = "Internship"

class JobStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    DRAFT = "draft"