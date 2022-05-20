from typing import Any, List
from .FieldSet import FieldSet

class Mapping(object):
    def __init__(self) -> None:
        self.list = FieldSet("List FieldSet", _for="List")
        self.retrieve = FieldSet("Retrieve FieldSet", _for="Retrieve")
        self.create = FieldSet("Create FieldSet", _for="Create")
        self.update = FieldSet("Update FieldSet", _for="Update")
        self.partial_update = FieldSet("PartialUpdate FieldSet", _for="Partial_Update")
        self.destroy = FieldSet("Destroy FieldSet", _for="Destroy")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError()

    def get_actions(self, ):
        return [ action for name, action in vars(self).items() if isinstance(action, FieldSet) ]
