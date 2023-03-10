"""
    공통으로 사용되는 custom classes
"""
from typing import List
from enum import Enum


class CustomEnum(Enum):
    @classmethod
    def name_list(cls) -> List:
        """return name list"""
        return [data.name for data in cls]

    @classmethod
    def value_list(cls) -> List:
        """return value list"""
        return [data.value for data in cls]

    def __eq__(self, other) -> bool:
        """check is equal with other value"""
        if isinstance(other, CustomEnum):
            return self is other
        if self.value == other:
            return True
        return False

    def __str__(self) -> str:
        return str(self.value)


class Test(CustomEnum):
    A = "a"
    B = "b"

