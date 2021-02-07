import inspect
from abc import ABC, abstractmethod
from typing import *

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django_hint import *
from rest_framework import serializers
from rest_framework.fields import empty

if TYPE_CHECKING:
    pass

__all__ = [
    "WritableSerializerMethodField", "WritableIDField",
    "WritableFromUserFieldMixin", "WritableAllFieldMixin", "UserRelationField"
]


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
        "object_not_found": _("Das Objekt wurde nicht gefunden"),
        "invalid_type": _("Ungültiger Typ")
    }
    
    @staticmethod
    def default_get_qs(key, request: RequestType, instance):
        raise NotImplementedError()
    
    def __init__(
            self,
            get_object: Optional[Callable] = None,
            lookup_field: str = "id",
            many: bool = False,
            detail: bool = False,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.get_object = get_object or self.default_get_qs
        self.lookup_field = lookup_field
        self.many = many
        self.detail = detail
        self.write_only = True
    
    def to_representation(self, value):
        raise NotImplementedError("to_representation shouldn't be called")
    
    def to_internal_value(self, data):
        if data is empty:
            self.fail("is_empty", input=data)
        
        if self.many:
            if not type(data) is list:
                self.fail("invalid_type", input=data)
            
            objs = []
            
            for single_data in data:
                try:
                    obj = self.get_object(single_data, self.context["request"], self)
                except ObjectDoesNotExist:
                    self.fail("object_not_found", input=single_data)
                else:
                    objs.append(obj)
            
            return objs
        else:
            try:
                return self.get_object(data, self.context["request"], self)
            except ObjectDoesNotExist:
                self.fail("object_not_found", input=data)


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


class UserRelationField(serializers.SerializerMethodField):
    @abstractmethod
    def default(self, obj: StandardModelType):
        raise NotImplementedError()
    
    def __init__(
            self,
            serializer: Type[serializers.Serializer],
            default: Union[dict, Callable],
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        
        self.default_value = default
        self.serializer = serializer
    
    def get_relation_object(self, model_obj) -> Optional[StandardModelType]:
        model = self.parent.Meta.model
        relation_model = self.serializer.Meta.model
        field_name = model.__name__.lower()
        user = self.context["request"].user
        
        try:
            relation_obj = relation_model.objects.only("user", field_name).get(**{
                "user": user,
                field_name: model_obj
            })
        except ObjectDoesNotExist:
            return
        else:
            return relation_obj
    
    def get_default_value(self, model: StandardModelType):
        if type(self.default_value) is dict:
            return self.default_value
        elif inspect.isfunction(self.default_value):
            return self.default_value(model, self)
        
        raise TypeError(f"`default_value` can either be a dict or function!")
    
    def to_representation(self, value):
        if obj := self.get_relation_object(value):
            return self.serializer(obj).data
        
        return self.get_default_value(value)
