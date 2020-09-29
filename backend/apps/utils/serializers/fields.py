from abc import ABC

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django_hint import *
from rest_framework import serializers

__all__ = [
    "RetrieveObjectByIDSerializerField", "WritableSerializerMethodField", "WritableIDField",
    "WritableFromUserFieldMixin", "WritableAllFieldMixin"
]

from rest_framework.fields import empty


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


class WritableSerializerMethodField(serializers.SerializerMethodField):
    def __init__(self, method_name: Optional[str] = None, *args, **kwargs):
        self.method_name = method_name
        self.setter_method_name = kwargs.pop('setter_method_name', None)
        self.deserializer_field = kwargs.pop('deserializer_field')
        
        kwargs.setdefault("read_only", False)
        read_only = kwargs.pop("read_only")
        
        kwargs['source'] = '*'
        super().__init__(*args, **kwargs)
        self.read_only = read_only
    
    def bind(self, field_name: str, parent):
        data = super().bind(field_name, parent)
        if not self.setter_method_name:
            self.setter_method_name = f'set_{field_name}'
        
        return data
    
    def to_internal_value(self, data):
        value = self.deserializer_field.to_internal_value(data)
        
        if hasattr(self.parent, self.setter_method_name):
            func = getattr(self.parent, self.setter_method_name)
            func(value)
        else:
            return {
                self.field_name: value
            }
        return {}


class WritableIDField(serializers.Field):
    default_error_messages = {
        "object_not_found": _("Das Objekt wurde nicht gefunden")
    }
    
    @staticmethod
    def default_get_qs(key, request: RequestType, instance):
        raise NotImplementedError()
    
    def __init__(
            self,
            get_object: Optional[Callable] = None,
            lookup_field: str = "id",
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.get_object = get_object or self.default_get_qs
        self.lookup_field = lookup_field
        self.__cached_object = None
    
    def run_validation(self, data=empty):
        if data is not empty:
            try:
                self.__cached_object = self.get_object(data, self.context["request"], self)
            except ObjectDoesNotExist:
                self.fail("object_not_found")
        
        return super().run_validation(data)
    
    def to_representation(self, value):
        return getattr(value, self.lookup_field)
    
    def to_internal_value(self, data):
        return self.__cached_object


class WritableFromUserFieldMixin(WritableIDField, ABC):
    model = Type[Model]
    lookup_field: str = "id"
    
    @classmethod
    def default_get_qs(cls, key, request: RequestType, instance):
        return cls.model.objects.from_user(request.user).only(cls.lookup_field).get(**{
            cls.lookup_field: key
        })


class WritableAllFieldMixin(WritableIDField, ABC):
    model = Type[Model]
    lookup_field: str = "id"
    
    @classmethod
    def default_get_qs(cls, key, request: RequestType, instance):
        return cls.model.objects.only(cls.lookup_field).get(**{
            cls.lookup_field: key
        })
