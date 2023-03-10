"""
    MongoDB connection

        - pymongo vs motor
            https://gist.github.com/anand2312/840aeb3e98c3d7dbb3db8b757c1a7ace
            https://motor.readthedocs.io/en/stable/differences.html
"""
import sentry_sdk
from typing import Union
from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.constants.settings import settings


# from app.main import conf
# from app.main import conf
# from app import con
# from app.common.configs import setting


# class MongoHandler(logging.Handler):
class MongoHandler:
    def __init__(self, database_name: Union[str, None] = None, collection_name: Union[str, None] = None):
        """
        init mongo handler

        :param database_name: mongodb database name
        :param collection_name: mongodb collection name
        :return:
        """
        self._client = None
        self._db = None
        self._collection = None
        self.connection(
            app_name=settings.app_name,
            host=settings.mongodb_host,
            port=settings.mongodb_port,
            username=settings.mongodb_username,
            password=settings.mongodb_password,
            database_name=database_name,
            collection_name=collection_name
        )

    def __del__(self):
        self.close()

    def connection(
        self,
        app_name: str,
        host: str,
        port: int,
        username: str,
        password: str,
        database_name: Union[str, None] = None,
        collection_name: Union[str, None] = None,
    ) -> None:
        """
        connect mongodb

        :param app_name: app name
        :param host: mongodb host
        :param port: mongodb port
        :param username: mongodb username
        :param password: mongodb password
        :param database_name: mongodb database name
        :param collection_name: mongodb collection name
        :return:
        """

        # client와 연결되어있는 경우 close
        if self._client:
            self.close()

        # mongodb 연결
        try:
            self._client = MongoClient(
                appname=app_name,
                host=host,
                port=port,
                username=username,
                password=password
            )

            if not bool(self._client.server_info()):
                raise Exception("mongodb server is not running")

            # get database if database_name exists
            if database_name:
                self._db = self._get_database(database_name)

            # get collection if collection_name exists
            if collection_name:
                self._collection = self._get_collection(collection_name)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            self.close()

    def close(self) -> None:
        """ close mongodb connection """
        self._client.close()
        self._client = None
        self._db = None
        self._collection = None

    def set_database(self, database_name: str) -> None:
        """
        database 설정

        :param database_name: database 명
        :return:
        """
        self._db = self._get_database(database_name)

    def set_collection(self, collection_name: str) -> None:
        """
        collection 설정

        :param collection_name: collection 명
        :return:
        """
        self._collection = self._get_collection(collection_name)

    def _get_database(self, database_name: str) -> Database:
        """
        database 조회 (존재하지 않을 경우, 생성)

        :param database_name: database 명
        :return: database
        """
        if database_name in self._client.list_database_names():
            return self._client.get_database(database_name)
        else:
            raise Exception("database does not exist")

    def _get_collection(self, collection_name: str) -> Collection:
        """
        collection 조회 (존재하지 않을 경우, 생성)

        :param collection_name: collection 명
        :return: collection
        """
        if collection_name in self._db.list_collection_names():
            return self._db.get_collection(collection_name)
        else:
            return self._db.create_collection(name=collection_name)


    def insert_one(self, document: dict) -> None:
        """
        데이터 삽입

        :param document: 삽입 데이터
        :return:
        """
        document["created_at"] = datetime.now()
        self._collection.insert_one(document)




# mongodb = MongoHandler(database_name=settings.mongodb_db_name)