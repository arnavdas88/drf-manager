from django import views
from rest_framework import serializers, viewsets, routers, permissions
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.response import Response

from django.db import models
from typing import Any, AnyStr, Dict, List, Union, Callable


class GenericViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get_view_name(self):
        return super().get_view_name()

    def get_view_description(self, html=False):
        return super().get_view_description(html)

    def get_queryset(self):
        self.parent_manager.request = self.request

        self.parent_manager.basename = self.basename
        self.parent_manager.action = self.action
        self.parent_manager.detail = self.detail
        self.parent_manager.suffix = self.suffix
        self.parent_manager.name = self.name
        self.parent_manager.description = self.description
        if hasattr(self, '__queryset__'):
            return getattr(self, '__queryset__')()
        return super().get_queryset()

    def get_object(self):
        self.parent_manager.request = self.request

        self.parent_manager.basename = self.basename
        self.parent_manager.action = self.action
        self.parent_manager.detail = self.detail
        self.parent_manager.suffix = self.suffix
        self.parent_manager.name = self.name
        self.parent_manager.description = self.description
        if hasattr(self, '__object__'):
            return getattr(self, '__object__')()
        return super().get_object()

    def get_permissions(self):
        self.parent_manager.request = self.request

        self.parent_manager.basename = self.basename
        self.parent_manager.action = self.action
        self.parent_manager.detail = self.detail
        self.parent_manager.suffix = self.suffix
        self.parent_manager.name = self.name
        self.parent_manager.description = self.description
        if hasattr(self, '__permissions__'):
            return getattr(self, '__permissions__')()
        return super().get_permissions()

    def get_renderers(self):
        self.parent_manager.request = self.request

        self.parent_manager.basename = self.basename
        self.parent_manager.action = self.action
        self.parent_manager.detail = self.detail
        self.parent_manager.suffix = self.suffix
        self.parent_manager.name = self.name
        self.parent_manager.description = self.description
        if hasattr(self, '__renderers__'):
            return getattr(self, '__renderers__')()
        return super().get_renderers()

    def get_authenticators(self):
        return super().get_authenticators()

    def get_parsers(self):
        return super().get_parsers()

    def get_parser_context(self, http_request):
        return super().get_parser_context(http_request)

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)

    def get_throttles(self):
        return super().get_throttles()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        self.parent_manager.request = self.request

        self.parent_manager.basename = self.basename
        self.parent_manager.action = self.action
        self.parent_manager.detail = self.detail
        self.parent_manager.suffix = self.suffix
        self.parent_manager.name = self.name
        self.parent_manager.description = self.description

        if hasattr(self, '__serializer__'):
            return getattr(self, '__serializer__')()

        return super().get_serializer_class()

    def get_serializer_context(self):
        return super().get_serializer_context()

    def dispatch(self, request, *args, **kwargs):

        self.parent_manager.args = self.args
        self.parent_manager.kwargs = self.kwargs
        self.parent_manager.raw_request = self.request

        return super().dispatch(request, *args, **kwargs)