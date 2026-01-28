from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from .auth_handler import decode_access_token
from ..db.base import AsyncSessionLocal


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if (
            request.url.path.startswith("/auth/register")
            or request.url.path == "/"
            or request.url.path.startswith("/auth/login")
            or request.url.path.startswith("/docs")
            or request.url.path.startswith("/openapi.json")
        ):
            return await call_next(request)

        auth_token = request.cookies.get("access_token")
        if not auth_token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authentication token missing"}
            )

        async with AsyncSessionLocal() as db:
            try:
                user = await decode_access_token(auth_token, db)
                request.state.uid = user.uid
            except Exception:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid authentication token"}
                )

        return await call_next(request)
