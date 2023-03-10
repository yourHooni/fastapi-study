"""
    error handler
"""
from typing import Union

from app.common.redis_handler import RedisHandler
from app.common.settings import settings


class ErrorCodeHandler:
    def __init__(self):
        self._code_redis = RedisHandler(
            host=settings.redis_host,
            db=5,
            username=settings.redis_username,
            password=settings.redis_password
        )

    def get_error_code_with_code(self, code: Union[str, int]):
        return self._code_redis.get_one("error_code_int", code)

    def get_error_code_with_str_code(self, code: str):
        return self._code_redis.get_one("error_code_str", code)

error_handler = ErrorCodeHandler()