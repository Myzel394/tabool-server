from typing import *

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, NotFound, ValidationError


class IdMixinSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
    )


class NestedSerializerMixin(serializers.ModelSerializer):
    @staticmethod
    def _is_pk_dict(data: dict, field: str = "id") -> bool:
        return field in data
    
    @staticmethod
    def __get_from_dict(data: dict, serializer_class: Type[serializers.Serializer], **kwargs):
        serializer_instance = serializer_class(data=data, **kwargs)
        serializer_instance.is_valid(raise_exception=True)
        instance = serializer_instance.save()
        
        return instance
    
    @staticmethod
    def __get_from_pk_dict(
            pk_dict: dict,
            serializer_class: Type[serializers.ModelSerializer],
            dict_pk_field: str = "id",
            pk_field: str = "id"
    ):
        model: models.Model = serializer_class.Meta.model
        pk = pk_dict[dict_pk_field]
        
        try:
            object = model.objects.get(**{
                pk_field: pk
            })
        except ObjectDoesNotExist:
            raise NotFound(f'Object with pk value "{pk}" not found.')
        
        return object
    
    @classmethod
    def __handle_raw_data(cls, raw_data, pk_field: str = "id", **kwargs):
        if cls._is_pk_dict(raw_data):
            return cls.__get_from_pk_dict(raw_data, dict_pk_field=pk_field, **kwargs)
        return cls.__get_from_dict(raw_data, **kwargs)
    
    @classmethod
    def create_nested(
            cls,
            serializer_class: Type[serializers.Serializer],
            raw: Union[dict, list],
            many: bool = False,
            pk_field: str = "id",
            **kwargs
    ) -> List[Type[models.Model]]:
        handle_kwargs = {
            "pk_field": pk_field,
            "serializer_class": serializer_class,
            **kwargs
        }
        
        if many:
            if not type(raw) is list:
                raise APIException(f"Data must be a list containing objects.")
            
            elements = []
            
            for raw_data in raw:
                elements.append(
                    cls.__handle_raw_data(raw_data, **handle_kwargs)
                )
            
            return elements
        else:
            if not type(raw) is dict:
                raise ValidationError(f"Data must be an object.", status.HTTP_400_BAD_REQUEST)
            
            return cls.__handle_raw_data(raw, **kwargs)
    
    @staticmethod
    def create_nested_by_ids(
            serializer_class: Type[serializers.ModelSerializer],
            ids: Sized,
            field: str = "id",
            **kwargs
    ):
        model: models.Model = serializer_class.Meta.model
        objects = model.objects.only(field).filter(**{
            f"{field}__in": ids
        })
        
        if objects.count() != len(ids):
            raise ValidationError("Couldn't find all elements based on ids.")
        
        serializer_instance = serializer_class(objects, **kwargs, many=True)
        serializer_instance.is_valid(raise_exception=True)
        instance = serializer_instance.save()
        
        return instance


class NestedModelSerializerField(serializers.SerializerMethodField):
    def __init__(
            self,
            serializer_class: Type[serializers.ModelSerializer],
            serializer_kwargs: Optional[Dict[str, Any]] = None,
            targeted_field: Optional[str] = None,
            input_methods: Optional[List[str]] = None,
            many: bool = False,
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
        serializer_instance = self.serializer_class(data=data, **self.serializer_kwargs)
        serializer_instance.is_valid(raise_exception=True)
        
        return serializer_instance.save()
    
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
        return self.serializer_class(
            getattr(instance, self.targeted_field_name),
            **self.serializer_kwargs
        ).data
    
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
