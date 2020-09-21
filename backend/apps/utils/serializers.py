from typing import *

from django.db import models
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError


class IdMixinSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
    )


class NestedModelSerializerField(serializers.Field):
    def __init__(
            self,
            serializer_class: Type[serializers.ModelSerializer],
            serializer_kwargs: Optional[Dict[str, Any]] = None,
            many: bool = False,
            targeted_field: Optional[str] = None,
            input_methods: Optional[List[str]] = None,
            pk_key: str = "id",
            filter_pk_key: Optional[str] = None,
            *args,
            **kwargs
    ):
        self.serializer_class = serializer_class
        self.serializer_kwargs = serializer_kwargs or {}
        self._targeted_field = targeted_field
        self.input_methods = input_methods or ["id", "data"]
        self.pk_key = pk_key
        self.filter_pk_key = filter_pk_key or pk_key
        self.many = many
        
        super().__init__(*args, **kwargs)
        
        self.read_only = kwargs.get("read_only", False)
    
    @property
    def targeted_field_name(self):
        return self._targeted_field or self.field_name
    
    def _is_pk_dict(self, data) -> bool:
        return self.pk_key in data and len(data) == 1
    
    def _handle_by_id(self, object_id: str):
        model: models.Model = self.serializer_class.Meta.model
        
        return model.objects.get(**{
            self.filter_pk_key: object_id
        })
    
    def _handle_by_dict(self, data: dict):
        kwargs = self.get_serializer_kwargs()
        serializer_instance = self.serializer_class(data=data, **kwargs)
        serializer_instance.is_valid(raise_exception=True)
        instance = serializer_instance.save()
        
        return instance
    
    def handle_data(self, data: dict):
        if self._is_pk_dict(data):
            if "id" not in self.input_methods:
                raise ValidationError("You are not allowed to pass ids.", status.HTTP_403_FORBIDDEN)
            
            return self._handle_by_id(data[self.pk_key])
        else:
            if "data" not in self.input_methods:
                raise ValidationError("You are not allowed to pass data as an object.", status.HTTP_403_FORBIDDEN)
            
            return self._handle_by_dict(data)
    
    def to_representation(self, instance):
        kwargs = self.get_serializer_kwargs()
        
        if self.many:
            instance = self.serializer_class(
                getattr(instance, self.targeted_field_name).all(),
                many=True,
                **kwargs
            )
        else:
            instance = self.serializer_class(
                getattr(instance, self.targeted_field_name),
                **kwargs
            )
        return instance.data
    
    def to_internal_value(self, _data):
        if self.many:
            if type(_data) is list:
                values = []
                
                for data in _data:
                    values.append(
                        self.handle_data(data)
                    )
                
                return values
            else:
                raise ValidationError("Input must be a list with data.")
        else:
            return self.handle_data(_data)
    
    def get_attribute(self, instance):
        return instance
    
    def get_serializer_kwargs(self) -> dict:
        return {
            "context": {
                **self.context,
                **self.serializer_kwargs.pop("context", {}),
            },
            **self.serializer_kwargs,
        }


class NestedModelParentSerializerMixin(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            if type(field) is NestedModelSerializerField:
                field.context.update(self.context)
