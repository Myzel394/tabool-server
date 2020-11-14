from abc import ABC
from typing import *

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django_hint import *
from rest_framework import serializers
from rest_framework.fields import empty

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

__all__ = [
    "RetrieveObjectByIDSerializerField", "WritableSerializerMethodField", "WritableIDField",
    "WritableFromUserFieldMixin", "WritableAllFieldMixin", "UserRelationField", "HistoryUserField"
]


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
    detail_serializer: Optional[Type[serializers.Serializer]] = None
    
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
    
    def to_representation(self, value):
        if not self.detail:
            return getattr(value, self.lookup_field)
        
        assert hasattr(self, "detail_serializer") and self.detail_serializer is not None, \
            f"No `detail_serializer` found on {self.__class__.__name__}."
        
        return self.detail_serializer(value, context=self.context).data
    
    def to_internal_value(self, data):
        if data is not empty:
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
    def __init__(self, serializer: Type[serializers.Serializer], *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.serializer = serializer
    
    def to_representation(self, value):
        user = self.context["request"].user
        relation = value.user_relations.get(user=user)
        
        return self.serializer(relation).data


class HistoryUserField(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["full_name", "id"]
    
    full_name = serializers.SerializerMethodField()
    
    def get_full_name(self, instance: "User"):
        return instance.get_full_name()
