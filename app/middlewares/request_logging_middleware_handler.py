"""
    Logging Request
"""
import time
from uuid import uuid4
import json

from starlette.middleware.base import RequestResponseEndpoint

from fastapi import FastAPI, Request, Response

from app.middlewares.base_http_middleware import BaseHTTPMiddleware
from app.common.mongodb import MongoHandler
from app.core.exception_handler import CustomException

class AsyncIteratorWrapper:
    """
        iterator to async iterator
        비동기 처리는 여러 개의 작업을 동시에 처리할 수 있어 처리 속도가 향상된다.
        https://www.python.org/dev/peps/pep-0492/#example-2
    """
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self._logdb = MongoHandler(database_name="logdb", collection_name="api_log")

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # TODO: 외부 api 호출 로그도 관리하려면 해당 request의 id를 가지고 있어야 좋을것 같음
        # 하지만, 현재 로직상 request_id가 mongodb에 적재시 생성되므로 어떻게 할지 고민 필요
        # 방안 1. uuid로 request_id 생성해서 관리 -> uuid는 유니크 하지 않음
        # 방안 2. request 받을시에 mongo에 적재하여 id를 생성하고 response 후 업데이트 -> 디비 액션이 한번 더 일어나야함
        request_id: str = str(uuid4())

        # await self.set_body(request)

        request_body = None
        try:
            request_body = await request.json()
        except Exception as e:
            print(e)

        is_success = True
        start_time = time.perf_counter()
        try:
            response: Response = await call_next(request)
            resp_status_code = response.status_code
            resp_body = [section async for section in response.__dict__["body_iterator"]]
            response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))

            try:
                resp_body = json.loads(resp_body[0].decode())
            except Exception:
                resp_body = str(resp_body)
        except CustomException as e:
            # TODO: error handling (with standard error code)
            is_success = False
            resp_body = str(e)
            resp_status_code = e.status_code.value
            response = Response(status_code=resp_status_code, content=e.to_json(), media_type="application/json")

        end_time = time.perf_counter()

        logging_dict = {
            "method": request.method,
            "path": request.url.path,
            "ip": request.client.host,
            "path_params": request.path_params,
            "query_params": request.query_params,
            "body": request_body,
            "status": is_success,
            "status_code": resp_status_code,
            "elapsed_time": f"{(end_time - start_time):.4f}",
            "response_body": resp_body
        }

        self._logdb.insert_one(logging_dict)
        return response

    # async def set_body(self, request: Request) -> None:
    #     receive_ = await request.receive()
    #
    #     async def receive() -> Message:
    #         return receive_
    #
    #     request._receive = receive
    #
    # async def _log_response(self, call_next: RequestResponseEndpoint, request: Request, request_id: str) \
    #         -> (Response, dict):
    #     start_time = time.perf_counter()
    #     response = await self._execute_request(call_next, request, request_id)
    #     end_time = time.perf_counter()
    #
    #     overall_status = "successful" if response.status_code < 400 else "failure"
    #     elapsed_time = end_time - start_time
    #
    #     response_logging = {
    #         "status": overall_status,
    #         "status_code": response.status_code,
    #         "elapsed_time": f"{elapsed_time:.4f}s",
    #     }
    #
    #     async for section in response.__dict__["body_iterator"]:
    #         print(section)
    #     resp_body = [section async for section in response.__dict__["body_iterator"]]
    #     response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))
    #
    #     try:
    #         resp_body = json.loads(resp_body[0].decode())
    #     except Exception:
    #         resp_body = str(resp_body)
    #
    #     response_logging["body"] = resp_body
    #
    #     return response, response_logging
    #
    # async def _execute_request(self, call_next: RequestResponseEndpoint, request: Request, request_id: str) -> Response:
    #     try:
    #         response: Response = await call_next(request)
    #
    #         response.headers["X-API-REQUEST-ID"] = request_id
    #         return response
    #     except Exception as e:
    #         self._logdb.insert_one(
    #             {
    #                 "request_id": request_id,
    #                 "path": request.url.path,
    #                 "method": request.method,
    #                 "detail": str(e)
    #             }
    #         )
    #         # self._logger.exception(
    #         #     {
    #         #         "request_id": request_id,
    #         #         "path": request.url.path,
    #         #         "method": request.method,
    #         #         "detail": e
    #         #     }
    #         # )


