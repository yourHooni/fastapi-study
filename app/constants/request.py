"""
    response 관련 constants
"""
from typing import Union
from dataclasses import dataclass

from app.constants.custom_class import CustomEnum


class HttpMethod(CustomEnum):
    """HTTP Method types"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    TRACE = "TRACE"
    OPTIONS = "OPTIONS"
    CONNECT = "CONNECT"

class StatusCode(CustomEnum):
    """status code"""

    HTTP_500 = 500
    HTTP_400 = 400
    HTTP_401 = 401
    HTTP_403 = 403
    HTTP_404 = 404
    HTTP_405 = 405
    HTTP_422 = 422


class ExceptionCode(CustomEnum):
    """exception code"""

    InvalidAccess = f"{StatusCode.HTTP_400}{'001'.zfill(4)}"
    NotExistData = f"{StatusCode.HTTP_400}{'410'.zfill(4)}"
    InvalidParams = f"{StatusCode.HTTP_400}{'201'.zfill(4)}"


@dataclass
class ErrorCode:
    """error code data"""

    error_code: str  # 에러 코드 (int)
    error_detail_code: str  # 에러 코드 (str)
    error_msg_en: str  # 영문 에러 메시지
    error_msg_kr: str  # 한글 에러 메시지
    reg_dt: int  # 생성일
    last_mod_dt: int  # 수정일
    error_detail_desc: Union[str, None] = None  # 에러 내용 상세
