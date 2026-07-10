from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "interview_portal"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SALT: str = "default_salt"

   
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    MONGO_DB_NAME: str
    LOG_LEVEL: str
    LOG_FILE: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        

settings = Settings()