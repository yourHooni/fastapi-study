import time
from typing import Optional

from fastapi import FastAPI, BackgroundTasks

from app.middlewares import http_middleware_handler
from app.middlewares.http_middleware_handler_base_http_middleware import BaseHTTPMiddleware
from app.middlewares.http_middleware_handler_base_http_middleware_origin \
    import BaseHTTPMiddleware as BaseHTTPMiddlewareOrigin
from app.middlewares.request_logging_middleware_handler import RequestLoggingMiddleware
from app.constants.settings import settings
from app.loggers import sentry_handler
from app.api.app import app_router
from app.api.v1.router import router as v1_router


#############################################################
# Exceptions


#############################################################


#############################################################
# Middlewares


#############################################################

#############################################################
# swagger configuration
swagger_config = {
    'displayRequestDuration': True,
    'docExpansion': 'none',
    'defaultModelExpandDepth': 0
}

# Set App

# initialize app
def get_application() -> FastAPI:
    # Set application
    application = FastAPI(
        title=f"{settings.app_name}: {settings.app_env}",
        version=settings.app_version,
        description="<a href='/apis/v1/docs'>API v1.0</a>",
        docs_url=settings.app_docs_url,
        redoc_url=settings.app_redoc_url,
        # contact={
        #     "name": settings.app_manager_name,
        #     "email": settings.app_manager_email,
        #     "url": settings.app_contact_url
        # },
        swagger_ui_parameters=swagger_config,
        debug=settings.app_debug
    )

    # Set sub applications
    sub_application_v1 = FastAPI(
        title=f"{settings.app_name} v1: {settings.app_env}",
        version=settings.app_version,
        description=""
    )
    sub_application_v1.include_router(v1_router)

    application.mount("/apis/v1", sub_application_v1)

    application.include_router(app_router)

    # set logger
    sentry_handler.init_sentry()

    return application

app = get_application()


# print(mongodb)

# set configs
# app.add_middleware(http_middleware_handler.CustomHttpMiddleware)
# app.add_middleware(http_middleware_handler.CustomHttpMiddleware2)
# app.add_middleware(BaseHTTPMiddleware)
# app.add_middleware(BaseHTTPMiddlewareOrigin)
# app.add_middleware(RequestLoggingMiddleware)

# app.router.route_class = CustomAPIRoute
#############################################################

#############################################################
# Decorators

#############################################################

