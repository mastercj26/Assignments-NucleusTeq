from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.exceptions.custom_exceptions import AppException
from src.schemas.response.common_response import ErrorResponse
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def register_exception_handlers(app):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        # log only method, path and status. no request body or user info (PII)
        logger.warning(
            "%s %s -> %s: %s", request.method, request.url.path, exc.status_code, exc.message
        )
        error = ErrorResponse(message=exc.message, status_code=exc.status_code)
        return JSONResponse(status_code=exc.status_code, content=error.model_dump())

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        error = ErrorResponse(message="Internal server error", status_code=500)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error.model_dump()
        )
