from django import views
from rest_framework import serializers, viewsets, routers, permissions
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import models
from typing import AnyStr, Dict, List, Mapping, Union, Callable

from .GenericViewSet import GenericViewSet
from .GenericSerializer import GenericSerializer

# "module/sys.modules" is a list of all the system files that are loading into memory at run time.
# There are for loops below that bolt the auto-generated ViewSets and Serializers to
# Django at runtime using the setattr() method.
import sys
module = sys.modules[__name__]

class APIManager():
    def __init__(self, model:Union[models.Model, models.query.QuerySet]=None, depth=2, *args, **kwargs):

        if isinstance(model, models.query.QuerySet):
            queryset = model
            model = queryset.model
        elif isinstance(model, models.Model):
            queryset = model.objects.all()

        self.model = model
        self.app_name = model._meta.app_label
        self.queryset = queryset

        self.exclude = None

        self.fields_mapping = {
            'list': '__all__',
            'retrieve': '__all__',
            'create': '__all__',
            'update': '__all__',
            'partial_update': '__all__',
            'destroy': '__all__',
        }
        self.serializer_mapping = {
            'list': None,
            'retrieve': None,
            'create': None,
            'update': None,
            'partial_update': None,
            'destroy': None,
        }

        self.nested_serializer = {
            'list': {},
            'retrieve': {},
            'create': {},
            'update': {},
            'partial_update': {},
            'destroy': {},
        }

        self.depth = 2

        # self.filterset_fields = ("country", "state", "city", )
        # self.search_fields = ("name", "email", )
        # self.ordering_fields = ("name", "country", )
        # self.ordering = ("-created_at", )

        self.viewset = None

    @property
    def fields(self, ):
        if hasattr(self, 'action'):
            return self.fields_mapping[self.action]
        return self.fields_mapping['list']

    @fields.setter
    def fields(self, value):
        self.fields_mapping = {
            'list': value,
            'retrieve': value,
            'create': value,
            'update': value,
            'partial_update': value,
            'destroy': value,
        }

    @fields.deleter
    def fields(self, ):
        self.fields_mapping = {
            'list': '__all__',
            'retrieve': '__all__',
            'create': '__all__',
            'update': '__all__',
            'partial_update': '__all__',
            'destroy': '__all__',
        }

    def get_queryset(self, ):
        return self.queryset

    def get_model(self, ):
        return self.model

    def get_serializers(self, ):
        return self.serializer_mapping[self.action]

    def get_viewset(self, ):
        return self.viewset

    def get_permissions(self, ):
        return [ permissions.AllowAny() ]

    def get_schema(self, ):
        return self.viewset.schema if self.viewset else None

    @classmethod
    def as_view(cls, *args, **kwargs):
        return super(viewsets.ModelViewSet, cls).as_view(*args, **kwargs)

    @action(detail=False)
    def dummy_action(self, request, *args, **kwargs):
        return Response({'status': 'success', 'action': 'dummy'})

    def get_actions(self, )->Dict[AnyStr, Callable]:
        """Returns all definitions decorated with `@action`

        Returns:
            Dict[AnyStr, Callable]: Returns a dictionary mapping the definition name with the definitions decorated with `@action`
        """
        # This below code to find the actions is not compatible with the inherited class ViewSetMixin
        # NOTE: Dead Code

        # field variables
        attrs = list(self.__dict__.keys())

        # all definitions without internal definitions and field variables
        definitions = [
            definition for definition in dir(self)
            if
            not definition.startswith('__') and
            definition not in attrs
        ]

        # get the actual definitions instead of the names
        definitions = [ getattr(self, definition) for definition in definitions ]

        # filter out all the actions from the definitions
        # NOTE: action definitions have attributes `mapping`, `url_path`, `url_path`, `kwargs` in them
        definitions = { definition.__name__:definition for definition in definitions if hasattr(definition, 'mapping') }

        return definitions

    def __call__(self, ) -> routers.BaseRouter:
        for action, fields in self.fields_mapping.items():
            nested_serializer = self.nested_serializer[action]
            self.serializer_mapping[action] = self.make_api_serializers(serializer_name= f'{self.model.__name__}{action.capitalize()}Serializer', fields=fields, nested_serializer=nested_serializer)

        self.viewset = self.make_api_viewsets()

        return self.make_api_router()

    def make_api_serializers(self, serializer_name:AnyStr=None, base_serializer_class:serializers.Serializer=GenericSerializer, fields:List[AnyStr]=None, nested_serializer:Mapping[str, serializers.Serializer] = {}) -> serializers.Serializer:
        """
        This function generates serializers for models returned in apps.apps.get_models()
        Adjusting the `depth` variable on Meta class can drastically speed up the API.
        It's recommended to use a customer Manager on each of your models to override
        `select_related` and `prefetch_related` and define which fields need joined there.

        Args:
            serializer_name (AnyStr, optional): Name of the serializer class
            base_serializer_class (serializers.Serializer, optional): Base class for the serializer. Defaults to GenericSerializer.
            fields (List[AnyStr], optional): List of fields to include during serialization

        Returns:
            serializers.Serializer: Serializer for the model.
        """

        # Create the serializer class
        class_name = f'{self.model.__name__}Serializer' if serializer_name is None else serializer_name
        fields_list = fields if fields else self.fields

        class ModelSerializer(base_serializer_class):
            class Meta:
                model = self.model

        ModelSerializer.Meta.depth = self.depth

        # fields inclusion - exclusion
        if fields_list =='__all__' and self.exclude:
            # use exclude instead of fields
            ModelSerializer.Meta.exclude = self.exclude
        else:
            # use fields instead of exclude
            if self.exclude:
                # if exclude exists, take that into account
                assert type(self.fields) is list
                for exclude in self.exclude:
                    if exclude in fields_list:
                        # exclude if exists
                        fields_list.remove(exclude)
            ModelSerializer.Meta.fields = fields_list

        # fields nested serialization
        for field in self.model._meta.get_fields():
            if field.name in fields_list:
                if field.name in nested_serializer:
                    if isinstance(field, models.ForeignKey):
                        field_serializer = nested_serializer[field.name]()
                        ModelSerializer._declared_fields[field.name] = field_serializer
                        # pass

                    if isinstance(field, models.ManyToManyField):
                        field_serializer = nested_serializer[field.name](many=True)
                        ModelSerializer._declared_fields[field.name] = field_serializer
                        # to = field.remote_field.model
                        # pass


        ModelSerializer.__name__ = class_name

        return ModelSerializer

    def make_api_viewsets(self, viewset_name:AnyStr=None, base_viewset_class:viewsets.GenericViewSet=GenericViewSet) -> viewsets.ViewSet:
        """
        This function generates ModelViewSets for models returned from apps.apps.get_models()

        Args:
            viewset_name (AnyStr, optional): Name of the viewset class
            base_viewset_class (viewsets.GenericViewSet, optional): Base class for the viewset. Defaults to GenericViewSet.

        Returns:
            viewsets.ViewSet: Viewset for the model
        """
        self.viewset = None
        ModelClass = self.model

        # Create the viewset class
        viewset_name = f'{ModelClass.__name__}ViewSet' if viewset_name is None else viewset_name
        viewset_bases = (base_viewset_class,)
        viewset_attrs = {
            # 'db_table': ModelClass._meta.db_table,
            # 'queryset': self.queryset,
            # 'serializer_class': api_serializer,
            # 'permission_classes': [],
            # 'action_permissions': {},
            'app_name': self.app_name,
            'get_queryset': self.get_queryset,
            'get_permissions': self.get_permissions,
            # 'get_serializer_class': self.get_serializers,
            '__serializer__': self.get_serializers,
            'parent_manager': self,
            **self.get_actions()
        }

        if self.get_schema():
            viewset_attrs['schema'] = self.get_schema()

        ModelViewSet = type(
            viewset_name,
            viewset_bases,
            viewset_attrs,
        )
        return ModelViewSet

    def make_api_router(self, router:routers.BaseRouter=None) -> routers.BaseRouter:
        """
        This function generates Router for viewsets dynamically

        Args:
            api_viewset (viewsets.ViewSet): Viewset needed to get routed
            router (routers.BaseRouter, optional): Predefined router where the route will be added

        Returns:
            routers.BaseRouter: Router with the route of the viewset
        """
        app_name = self.app_name
        model_name = self.model.__name__

        rest_api_urls = [
            (fr'{model_name}', self.viewset, f'{app_name}.{model_name}')
        ]

        # Create the router
        router = router if router else routers.DefaultRouter()
        for route in rest_api_urls:
            router.register(route[0], route[1], basename=route[2])

        return router
