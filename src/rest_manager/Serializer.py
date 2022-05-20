from typing import Any
from .Mapping import Mapping
from .utils import get_model_fields
from django.db.models import Model

class SerializerDefinition(Mapping):

    def __init__(self, base_object:Model) -> None:
        self.allowed_fields = get_model_fields(base_object)
        self._fields = "__all__"
        self.exclude = []

        super().__init__()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)

    @property
    def fields(self, ):
        return self._fields

    @fields.setter
    def fields(self, value):
        for action in self.get_actions():
            if action.fields is None:
                action.fields = value
        self._fields = value

    def build_fieldset(self, ):
        for action in self.get_actions():
            # _fields represent the default fieldset for all actions
            action.build(self.allowed_fields, default_fieldset = self.fields, exclude_fieldset=self.exclude)