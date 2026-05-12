import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .tracing import correlation_id_ctx

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-Id", str(uuid.uuid4()))
        token = correlation_id_ctx.set(correlation_id)
        
        try:
            response = await call_next(request)
            response.headers["X-Correlation-Id"] = correlation_id
            return response
        finally:
            correlation_id_ctx.reset(token)
