from typing import List
from django.db.models import Model
from django.db.models.fields import related

def get_model_fields(model:Model) -> List:
    return [ field.name for field in model._meta.get_fields() if not isinstance(field, related.ForeignObjectRel) ]

def validate(fieldset, allowed_fields, raise_exception=False):
    for field in fieldset:
        if field not in allowed_fields:
            if raise_exception:
                raise Exception(f"The field {field} not found.")
            else:
                return False
    return True