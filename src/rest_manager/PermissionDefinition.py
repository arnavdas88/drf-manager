from typing import Any

from django.db.models import Model

from .Mapping import Mapping
from .PermissionSet import PermissionSet
from .utils import get_model_fields

class PermissionDefinition(Mapping):
    def __init__(self, ) -> None:
        self._permissions = []

        self.list = []
        self.retrieve = []
        self.create = []
        self.update = []
        self.partial_update = []
        self.destroy = []

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)

    @property
    def permissions(self, ):
        return self._permissions

    @permissions.setter
    def permissions(self, value):
        self._permissions = value


    def get_actions(self, ):
        return [ action for name, action in vars(self).items() if isinstance(action, list) ]

    def get_action(self, action):
        actions = [ action_fieldset for name, action_fieldset in vars(self).items() if isinstance(action_fieldset, list) and name is action ]
        if len(actions) == 1:
            return actions[0]
        if len(actions) > 1:
            raise Exception(f"Ambiguous name {action} exists.")
        return []

