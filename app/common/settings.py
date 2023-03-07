"""
    https://fastapi.tiangolo.com/advanced/settings/

    App Setting 관리
"""
from pathlib import Path
from functools import lru_cache

from pydantic import BaseSettings

from app.constants.env import Env


parent_path = Path.cwd()

class Settings(BaseSettings):
    parent_path = Path.cwd()

    # app settings
    app_env: Env = Env.DEV
    debug: bool = False
    app_name: str = ""
    app_version: float = 0.00
    app_docs_url: str = "/docs"
    app_redoc_url: str = "/redoc"
    app_manager_name: str = "manager"
    app_manager_email: str = "email"
    app_contact_url: str = "contact_url"

    # mongodb settings
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_username: str = "root"
    mongodb_password: str = "root"

    class Config:
        env_file = [
            f"{parent_path}/.env/{file_name}"
            for file_name in ["app.env", "mongodb.env"]
        ]

    def __post_init__(self):
        self.debug = self.app_env in (Env.DEV, Env.STAGING)


@lru_cache()
def get_settings():
    """
    setting 정보 조회

    :return: setting 데이터
    """
    # from app.schemas.settings import Settings
    print("get setting...")
    return Settings()


settings = Settings()