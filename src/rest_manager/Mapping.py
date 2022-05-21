from typing import Any, List, Type
from .FieldSet import FieldSet

class Mapping(object):
    def __init__(self, T:Type) -> None:
        TName = T.__name__
        self.list = T(f"List {TName}", _for="List")
        self.retrieve = T(f"Retrieve {TName}", _for="Retrieve")
        self.create = T(f"Create {TName}", _for="Create")
        self.update = T(f"Update {TName}", _for="Update")
        self.partial_update = T(f"PartialUpdate {TName}", _for="Partial_Update")
        self.destroy = T(f"Destroy {TName}", _for="Destroy")
        self.metadata = T(f"Metadata {TName}", _for="Metadata")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError()

    def get_actions(self, ):
        return [ action for name, action in vars(self).items() if isinstance(action, FieldSet) ]

    def get_action(self, action):
        actions = [ action_fieldset for name, action_fieldset in vars(self).items() if isinstance(action_fieldset, FieldSet) and name is action ]
        if len(actions) == 1:
            return actions[0]
        if len(actions) > 1:
            raise Exception(f"Ambiguous name {action} exists.")
        raise Exception(f"Cannot find the action {action}.")