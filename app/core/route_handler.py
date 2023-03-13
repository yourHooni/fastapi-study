"""
    route를 관리하는 handler를 정의한다.
"""
import time
from typing import Callable
import gzip

from starlette.types import Receive, Scope
from fastapi import Request, Response
from fastapi.routing import APIRoute

from app.core.mongodb import MongoHandler
from app.core.custom_exception import CustomException


class CustomRequest(Request):
    def __init__(
            self, scope: Scope, receive: Receive
    ):
        super().__init__(scope, receive)
        self._body = None

    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class CustomAPIRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        self._logdb = MongoHandler(database_name="logdb", collection_name="api_log")
        super().__init__(*args, **kwargs)

    def get_route_handler(self) -> Callable:
        route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # TODO: 외부 api 호출 로그도 관리하려면 해당 request의 id를 가지고 있어야 좋을것 같음
            # 하지만, 현재 로직상 request_id가 mongodb에 적재시 생성되므로 어떻게 할지 고민 필요
            # 방안 1. uuid로 request_id 생성해서 관리 -> uuid는 유니크 하지 않음
            # 방안 2. request 받을시에 mongo에 적재하여 id를 생성하고 response 후 업데이트 -> 디비 액션이 한번 더 일어나야함
            # request = CustomRequest(request.scope, request.receive)
            request_body = None

            is_success = True
            start_time = time.perf_counter()
            try:
                response: Response = await route_handler(request)
                resp_status_code = response.status_code
                resp_body = response.body
            except CustomException as e:
                is_success = False
                resp_body = str(e)
                resp_status_code = e.status_code.value
                response = Response(
                    status_code=resp_status_code,
                    content=e.to_json(),
                    media_type="application/json"
                )
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
                "response_body": resp_body,
            }

            self._logdb.insert_one(logging_dict)
            return response


        return custom_route_handler

# router = APIRouter(route_class=CustomAPIRoute)

