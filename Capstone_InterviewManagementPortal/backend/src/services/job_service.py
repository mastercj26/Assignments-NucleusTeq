from src.repositories.job_repository import JobRepository

class JobService:

    @staticmethod
    def create_job(job_data: dict):
        return JobRepository.create(job_data)

    @staticmethod
    def get_all_jobs(page: int = 1, per_page: int = 10):
        skip = (page - 1) * per_page
        jobs = JobRepository.get_all(skip=skip, limit=per_page)
        total = JobRepository.count()
        return {
            "jobs": jobs,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page
        }

    @staticmethod
    def get_job_by_id(job_id: str):
        return JobRepository.get_by_id(job_id)

    @staticmethod
    def update_job(job_id: str, update_data: dict):
        return JobRepository.update(job_id, update_data)