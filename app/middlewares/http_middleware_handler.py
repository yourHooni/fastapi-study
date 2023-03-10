"""
    CustomHttpMiddleware
"""
import time

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

from fastapi import FastAPI, Request, Response

from app.middlewares.base_http_middleware import BaseHTTPMiddleware


class CustomHttpMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            request.state.start = time.time()
            request.state.user = None

            # set config (secret manager handler)

            # token 체크 (여기에서 request가 아닌 session을 사용하는건 어떤지?)

            response = await call_next(request)

            # 로그

            return response
        except Exception as e:
            print(e)

            # 로그

            return JSONResponse(
            )

