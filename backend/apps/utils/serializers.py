from typing import *

from django.db import models
from django_hint import QueryType
from rest_framework import serializers


class IdMixinSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
    )


class NestedSerializerMixin(serializers.ModelSerializer):
    @staticmethod
    def create_nested(serializer_class: Type[serializers.Serializer], raw: dict, **kwargs) -> Type[models.Model]:
        serializer_instance = serializer_class(data=raw, **kwargs)
        serializer_instance.is_valid(raise_exception=True)
        instance = serializer_instance.save()
        
        return instance
    
    @staticmethod
    def create_by_ids(ids: Iterable[Any], queryset: QueryType, id_field: str = "id"):
        pass
