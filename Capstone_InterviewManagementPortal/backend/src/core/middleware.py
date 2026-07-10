from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.security import decode_access_token
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

PUBLIC_PATHS = {
    "/",
    "/health",
    "/auth/login",
    "/auth/reset-password",
    "/api/docs",
    "/api/redoc",
    "/openapi.json",
}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        
        if request.url.path.startswith("/api/docs") or request.url.path.startswith("/openapi.json"):
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Not authenticated")

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        token = parts[1]
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        
        request.state.user = payload
        return await call_next(request)