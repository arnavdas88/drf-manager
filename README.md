# drf-manager
Django Rest Framework API Manager. Manages most of the structural basics, automatically.


![PRs welcome!](https://img.shields.io/badge/PRs-welcome!-success)

## Setup

To add the `rest_manager` to your project, install it using [pip](https://pip.pypa.io/):

Installing from Source
```bash
pip3 install git+https://github.com/arnavdas88/drf-manager
```

## Example

Then import it like any other module:

```python
from rest_manager.APIManager import APIManager
from rest_manager.GenericViewSet import GenericViewSet
```


Once the import is done, we can just use a few lines of code to build the Viewsets, Serializers and Routers

```python
manager = APIManager(User)
manager.fields = ['id', 'username', 'first_name']
manager.detail_fields = '__all__'

router = manager()
```

The Manager could be used with both, Models and QuerySets

```python
manager = APIManager(User.objects.filter(is_staff=True))
```


Some Helper functions:

```python
from rest_manager.contrib.auth import get_model_manager

get_user_model = get_model_manager('User')
get_organization_model = get_model_manager('Organization')
```

If you prefer to add the package manually or just want to examine the source code, see [DRF Manager on GitHub](https://github.com/arnavdas88/drf-manager).