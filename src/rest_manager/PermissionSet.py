from enum import Enum
from typing import Any, List

from .SetDefinition import SetDefinition

class PermissionSet(SetDefinition, ):
    def __init__(self, name, _for=None):
        super().__init__(name, _for)


    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

