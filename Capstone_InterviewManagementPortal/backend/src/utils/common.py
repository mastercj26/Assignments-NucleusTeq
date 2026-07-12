RESUME_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
RESUME_MIN_SIZE = 100  # bytes


def normalize_email(email: str) -> str:
    return email.strip().lower()
