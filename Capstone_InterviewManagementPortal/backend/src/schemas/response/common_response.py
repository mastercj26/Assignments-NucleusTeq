from pydantic import BaseModel


class GenericMessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    status_code: int


class ResumeUploadResponse(BaseModel):
    file_id: str
    filename: str
