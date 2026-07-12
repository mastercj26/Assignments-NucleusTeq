from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.security import decode_access_token
from src.schemas.response.common_response import ErrorResponse

PUBLIC_PATHS = {
    "/",
    "/health",
    "/auth/login",
    "/auth/reset-password",
    "/openapi.json",
}
PUBLIC_PREFIXES = ("/api/docs", "/api/redoc")


def _unauthorized(message: str) -> JSONResponse:
    error = ErrorResponse(message=message, status_code=401)
    return JSONResponse(status_code=401, content=error.model_dump())


class AuthMiddleware(BaseHTTPMiddleware):
    """Checks the bearer token for all protected paths and puts the
    decoded user on request.state. Role checks are done per route."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if request.method == "OPTIONS" or path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES):
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return _unauthorized("Not authenticated")
        token = parts[1]

        payload = decode_access_token(token)
        if not payload:
            return _unauthorized("Invalid or expired token")

        request.state.user = payload
        return await call_next(request)
