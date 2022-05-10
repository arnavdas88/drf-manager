from typing import Any


class Mapping(object):
    mapping = {
        'list': None,
        'retrieve': None,
        'create': None,
        'update': None,
        'partial_update': None,
        'destroy': None,
    }
    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
