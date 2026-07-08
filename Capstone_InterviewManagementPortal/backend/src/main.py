from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   
from src.core.database import Database
from src.exceptions.exception_handlers import register_exception_handlers
from src.routers.auth_router import router as auth_router
import logging
from src.routers import auth_router, user_router, job_router, candidate_router
from src.utils.logger import setup_logger
from src.routers import interview_router, feedback_router, dashboard_router
logger = setup_logger(__name__)
app = FastAPI(
    title="Interview Management Portal API",
    description="Backend APIs for managing interviews, candidates, and feedback.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)         

register_exception_handlers(app)

@app.on_event("startup")
async def startup():
    logger.info("Starting up...")
    
    Database.connect()

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down...")
    
    if Database.client:
        Database.client.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Interview Management Portal API"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(job_router)
app.include_router(candidate_router)
app.include_router(interview_router)
app.include_router(feedback_router)
app.include_router(dashboard_router)