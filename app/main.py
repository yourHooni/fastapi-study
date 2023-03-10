import time
from typing import Optional

from fastapi import FastAPI, BackgroundTasks

from app.middlewares import http_middleware_handler
from app.middlewares.http_middleware_handler_base_http_middleware import BaseHTTPMiddleware
from app.middlewares.http_middleware_handler_base_http_middleware_origin \
    import BaseHTTPMiddleware as BaseHTTPMiddlewareOrigin
from app.common.settings import settings
from app.loggers import sentry_handler


#############################################################
# Exceptions


#############################################################


#############################################################
# Middlewares


#############################################################

#############################################################
# Set App

app = FastAPI()

app.add_middleware(http_middleware_handler.CustomHttpMiddleware)
app.add_middleware(http_middleware_handler.CustomHttpMiddleware2)
# set logger
sentry_handler.init_sentry()
# app.add_middleware(BaseHTTPMiddleware)
# app.add_middleware(BaseHTTPMiddlewareOrigin)

#############################################################

#############################################################
# Decorators

#############################################################


#############################################################
# Set API

def background_task_test():
    time.sleep(5)
    print("background_task_test")


@app.get("/")
def read_root(background_tasks: BackgroundTasks):
    print("read root")
    background_tasks.add_task(background_task_test)
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/test")
def test_api():
    return {"Test": "This is Test"}

@app.get("/app_info")
def get_app_info():
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "app_env": settings.app_env
    }
#############################################################
