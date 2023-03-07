"""
    실행 환경
"""
from app.constants.custom_class import CustomEnum


class Env(CustomEnum):
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"
