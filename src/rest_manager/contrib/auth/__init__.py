from typing import Callable, AnyStr
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied

def get_model_manager(model_name:AnyStr)->Callable:
    """Generates a model manager to equivalent to `get_user_model()` for virtually any other model.

    Args:
        model_name (AnyStr): Model name for which we want to build the manager

    Returns:
        Callable: The callable definition like `get_user_model()`
    """    
    variable_name = model_name.upper() + "_MODEL"
    definition_name = model_name.lower()

    def get_x_model():
        f"""
        Return the {variable_name} model that is active in this project.
        """
        model = getattr(settings, variable_name)
        try:
            return django_apps.get_model(model, require_ready=False)
        except ValueError:
            raise ImproperlyConfigured(
                f"{variable_name} must be of the form 'app_label.model_name'"
            )
        except LookupError:
            raise ImproperlyConfigured(
                "{variable_name} refers to model '%s' that has not been installed"
                % model
            )
    
    get_x_model.__doc__ = f"Return the {model_name} model that is active in this project."
    get_x_model.__name__ = f"get_{definition_name}_model"
    
    return get_x_model