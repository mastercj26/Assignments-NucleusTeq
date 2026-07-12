from src.repositories.job_repository import JobRepository


class JobService:

    @staticmethod
    def create_job(data: dict) -> dict:
        return JobRepository.create(data)

    @staticmethod
    def get_all_jobs(page: int = 1, per_page: int = 10) -> dict:
        skip = (page - 1) * per_page
        jobs = JobRepository.get_all(skip=skip, limit=per_page)
        total = JobRepository.count()
        return {
            "jobs": jobs,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": max(1, (total + per_page - 1) // per_page),
        }

    @staticmethod
    def get_job_by_id(job_id: str) -> dict:
        return JobRepository.get_by_id(job_id)

    @staticmethod
    def update_job(job_id: str, data: dict) -> dict:
        return JobRepository.update(job_id, data)
