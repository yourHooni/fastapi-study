"""
    error handler
"""
import json
from typing import Union

from app.common.error_handler import error_handler
from app.constants.response import StatusCode, ExceptionCode, ErrorCode


class CustomException(Exception):
    """custom exception"""

    status_code: StatusCode
    code: str
    exception_code: str
    message: Union[str, None] = None
    description: Union[str, None] = None

    def __init__(
        self, exception_code: ExceptionCode, description: Union[str, None] = None
    ):
        error_code: ErrorCode = ErrorCode(
            **error_handler.get_error_code_with_code(exception_code.value)
        )
        self.code = error_code.error_code
        self.status_code = StatusCode(int(self.code[:3]))
        self.exception_code = error_code.error_detail_code
        self.description = description or error_code.error_detail_desc
        self.message = error_code.error_msg_kr

    def to_dict(self) -> dict:
        """data to dict"""
        return {
            "status_code": self.status_code.value,
            "code": self.code,
            "exception_code": self.exception_code,
            "message": self.message,
            "description": self.description,
        }

    def to_json(self) -> json:
        """data to json"""
        return json.dumps(self.to_dict())
