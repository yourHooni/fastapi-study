from fastapi import APIRouter

from app.core.route import CustomAPIRoute
from app.constants.settings import settings


app_router = APIRouter(route_class=CustomAPIRoute)

#################################################################################################
# App APIs
#################################################################################################
@app_router.get("/app_info", name="앱 정보 조회")
def get_app_info_api():
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "app_env": settings.app_env
    }

@app_router.get("/health", name="서버 동작 체크")
def check_health_api():
    return True