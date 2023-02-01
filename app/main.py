import time
from typing import Optional

from fastapi import FastAPI, BackgroundTasks

from app.middlewares.http_middleware_handler_base_http_middleware import BaseHTTPMiddleware
from app.middlewares.http_middleware_handler_base_http_middleware_origin \
    import BaseHTTPMiddleware as BaseHTTPMiddlewareOrigin


#############################################################
# Exceptions


#############################################################


#############################################################
# Middlewares


#############################################################

#############################################################
# Set App

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware)
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
    background_tasks.add_task(background_task_test)
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/test")
def test_api():
    return {"Test": "This is Test"}
#############################################################
