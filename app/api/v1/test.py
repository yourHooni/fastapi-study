import time
from typing import Union

from fastapi import APIRouter, BackgroundTasks

from app.core.custom_exception import CustomException
from app.constants.response import ExceptionCode
from app.core.route_handler import CustomAPIRoute


test_router = APIRouter(route_class=CustomAPIRoute)

#################################################################################################
# Test APIs
#################################################################################################
def background_task_test():
    time.sleep(5)
    print("background_task_test")


@test_router.get("/")
def read_root(background_tasks: BackgroundTasks):
    print("read root")
    background_tasks.add_task(background_task_test)
    return {"Hello": "World"}


@test_router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@test_router.get("/test")
def test_api():
    return {"Test": "This is Test"}

@test_router.get("/error_test", name="error_test")
def error_test():
    raise CustomException(exception_code=ExceptionCode.InvalidAccess)
