from rest_framework.serializers import Serializer as DRF_SERIALIZER
from django.db.models import fields as DJANGO_FIELDS
from django.db.models.fields import Field

from enum import Enum
from typing import Any, List

from .GenericSerializer import GenericSerializer
from .utils import validate

class SerializerScheme(Enum):
    Field = "fields"
    Exlcuded = "exclude"

class FieldSet:
    def __init__(self, name, _for=None) -> None:
        self.name = name
        self._for = _for

        # Fields to be shown
        self.fields = None
        self.validated_fieldset = None

        # Serializer override for its fields
        self._serializer_for_field = {}

        # Original Serializer
        self._serializer:GenericSerializer = None

        # This specifies if the serializer is exclude based or fields based
        self.scheme = SerializerScheme.Field # Scheme : "exclude" or "field"

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def build(self, allowed_fields:List, default_fieldset:List = [], exclude_fieldset:List = None, prefered_scheme:SerializerScheme = SerializerScheme.Field) -> None:
        fields = default_fieldset if self.fields is None else self.fields

        if fields == "__all__" and exclude_fieldset:
            # excludes
            validate(exclude_fieldset, allowed_fields, raise_exception=True)
            self.scheme = SerializerScheme.Exlcuded
            self.validated_fieldset = exclude_fieldset
        elif not exclude_fieldset:
            # fields
            if fields != "__all__":
                validate(fields, allowed_fields, raise_exception=True)
            self.scheme = SerializerScheme.Field
            self.validated_fieldset = fields
        else:
            # fields
            if exclude_fieldset:
                validate(exclude_fieldset, allowed_fields, raise_exception=True)
            if fields:
                validate(fields, allowed_fields, raise_exception=True)

            # apply exclude
            for field in exclude_fieldset:
                if field in fields:
                    fields.remove(field)

            self.scheme = SerializerScheme.Field
            self.validated_fieldset = fields

    @property
    def serializer(self, ):
        return self._serializer

    @serializer.setter
    def serializer(self, value):
        self._serializer = value

    def define_serializer(self, field, serializer):
        if isinstance(serializer, DRF_SERIALIZER):
            self._serializer_for_field[field] = serializer
        elif isinstance(serializer, FieldSet):
            self._serializer_for_field[field] = serializer.serializer



