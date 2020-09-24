from abc import ABC, abstractmethod
from typing import *

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django_hint import StandardModelType
from rest_framework import serializers
from rest_framework.response import Response


class RandomIDSerializerMixin(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
    )


class AssociatedUserSerializerMixin(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        validated_data.pop("associated_user", None)
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        validated_data["associated_user"] = self.context["request"].user


class RetrieveObjectByIDSerializerField(serializers.CharField):
    def __init__(self, retrieve_func: Callable[[str, "RetrieveObjectByIDSerializerField"], None], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._retrieve_func = retrieve_func
    
    def run_validation(self, data):
        value = super().run_validation(data)
        
        try:
            obj = self._retrieve_func(value, self)
        except ObjectDoesNotExist:
            self.fail("object_not_found")
        
        return obj


class ReferencedObjectViewSetMixin:
    validated_data_key: str
    validate_serializer_class: Type[serializers.Serializer]
    referenced_object_lookup_field: str = "pk"
    
    @abstractmethod
    def get_referenced_queryset(self) -> QuerySet:
        raise NotImplementedError()
    
    def get_referenced_object(self, validated_value: Dict[str, Any]):
        try:
            return self \
                .get_referenced_queryset() \
                .only(self.referenced_object_lookup_field) \
                .get(**{self.referenced_object_lookup_field: validated_value[self.validated_data_key]})
        except ObjectDoesNotExist:
            raise ValidationError(_("Das Element konnte nicht gefunden werden."), "reference_not_found")
    
    def parse_to_get_referenced_object(self, request: WSGIRequest) -> StandardModelType:
        serializer = self.validate_serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        obj = self.get_referenced_object(validated_data)
        
        return obj
    
    def list_response_from_qs(self, queryset: QuerySet):
        # Output
        queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
