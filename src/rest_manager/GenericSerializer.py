
from typing import Dict, OrderedDict
from django.conf import settings
from django.db.models import QuerySet, query
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status, mixins, parsers, serializers
from rest_framework.generics import get_object_or_404

class GenericSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        return super().validate(attrs)

    def to_internal_value(self, data) -> OrderedDict:
        """
        Dict of native values <- Dict of primitive datatypes.
        """
        return super().to_internal_value(data)
    
    def to_representation(self, instance) -> Dict:
        """
        Object instance -> Dict of primitive datatypes.
        """
        return super().to_representation(instance)
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
