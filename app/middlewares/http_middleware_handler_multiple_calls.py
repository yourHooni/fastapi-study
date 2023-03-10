"""
    - call_next (실행 api)
        * BaseHttpMiddleware를 여러번 호출해도 call_next가 한번만 호출되는 이유
            call_next가 실행될때, 다음 미들웨어를 호출한다.
            마지막 미들웨어에 도달할 경우, 해당 미들웨어 실행 후 이전 작업을 실행한다.
"""

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from fastapi import FastAPI, Request, Response

from app.middlewares.base_http_middleware import BaseHTTPMiddleware


class CustomHttpMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        print("1")
        response = await call_next(request)
        response.headers['Custom1'] = 'Example'
        return response


class CustomHttpMiddleware2(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        print("2")
        response = await call_next(request)
        response.headers['Custom2'] = 'Example2'
        return response
