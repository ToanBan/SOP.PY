from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from src.pkg.config.settings import settings

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        # response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' data: {settings.MINIO_URL}; "
            "script-src 'self'; "
            "style-src 'self'; "
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response