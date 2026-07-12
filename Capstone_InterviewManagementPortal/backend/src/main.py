from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.database import Database
from src.core.middleware import AuthMiddleware
from src.exceptions.exception_handlers import register_exception_handlers
from src.routers import (
    auth_router,
    candidate_router,
    dashboard_router,
    feedback_router,
    interview_router,
    job_router,
    user_router,
)
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Fail fast if the database is unreachable rather than erroring on
    # the first request. The URI is deliberately not logged (credentials).
    Database.ping()
    logger.info("MongoDB connection verified (database: %s)", settings.MONGO_DB_NAME)
    yield
    logger.info("Closing MongoDB connection")
    Database.close()


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend APIs for managing jobs, candidates, interviews and feedback.",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(job_router)
app.include_router(candidate_router)
app.include_router(interview_router)
app.include_router(feedback_router)
app.include_router(dashboard_router)


@app.get("/", tags=["Health"])
def root():
    return {"message": f"{settings.APP_NAME} API is running"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "OK"}
