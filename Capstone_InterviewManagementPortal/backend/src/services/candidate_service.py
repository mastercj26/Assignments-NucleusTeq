from src.repositories.candidate_repository import CandidateRepository
from src.exceptions.custom_exceptions import ValidationException, NotFoundException

class CandidateService:
   
    MAX_RESUME_SIZE = 5 * 1024 * 1024  # 5 MB

    @staticmethod
    def upload_resume(candidate_id: str, file_data: bytes, filename: str):
        """Upload resume file after validating size and content."""
    
        if not filename.lower().endswith('.pdf'):
            raise ValidationException("Only PDF files are allowed")

   
        if not file_data or len(file_data) == 0:
            raise ValidationException("Uploaded file is empty")
        def is_pdf(data: bytes) -> bool:
          return data[:4] == b'%PDF'

      
        if len(file_data) > CandidateService.MAX_RESUME_SIZE:
            raise ValidationException(
                f"File size exceeds maximum allowed ({CandidateService.MAX_RESUME_SIZE // (1024*1024)} MB)"
            )

        
        CandidateRepository.get_by_id(candidate_id)


        file_id = CandidateRepository.save_resume(candidate_id, file_data, filename)
        return {"file_id": file_id, "filename": filename}