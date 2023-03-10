"""
    Redis Connection
"""
import json
import sentry_sdk
import redis
from typing import Union, List


class RedisHandler:
    def __init__(self, host: str, db: int, username: str, password: str):
        """
        init redis handler

        :param host: redis host
        :param db: redis db
        :param username: redis username
        :param password: redis password
        :return:
        """
        self._client = None
        self.connection(
            host=host,
            db=db,
            username=username,
            password=password
        )

    def __del__(self):
        self.close()

    def connection(
        self,
        host: str,
        db: int,
        username: str,
        password: str
    ) -> None:
        """
        connect redis

        :param host: redis host
        :param db: redis db
        :param username: redis username
        :param password: redis password
        :return:
        """
        # client와 연결되어있는 경우 close
        if self._client:
            self.close()

        # redis 연결
        try:
            self._client = redis.Redis(
                host=host,
                db=db,
                encoding="utf-8",
                ssl=True,
                decode_responses=True,
                username=username,
                password=password
            )
            if not bool(self._client.ping()):
                raise Exception("Redis connection failed")

        except Exception as e:
            sentry_sdk.capture_exception(e)
            self.close()

        print(self._client)

    def close(self) -> None:
        """ close redis connection """
        self._client.close()
        self._client = None

    # TODO: 리턴 타입 고민..
    def get_all_dict(self, name: str) -> Union[dict, List, None]:
        data = self._client.hgetall(name)
        return data
        # if isinstance(data, dict):
        #     return data
        # else:
        #     # TODO: type이 다른 경우 처리 방법 구현
        #     return {}

    def get_one(self, name: str, field: str) -> Union[dict, None]:
        data = self._client.hget(name, field)
        if isinstance(data, str):
            try:
                return json.loads(data)
            except Exception as e:
                sentry_sdk.capture_exception(e)
                return None
        return data

    # def get_all_dict(self, name: str) -> List:
    #     data = self._client.hgetall("error_code_str")
    #     if isinstance(data, dict):
    #         return data
    #     else:
    #         # TODO: type이 다른 경우 처리 방법 구현
    #         return {}
    #

    # def get(self, key: str) -> Union[str, None]:

