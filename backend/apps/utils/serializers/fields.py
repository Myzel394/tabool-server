from typing import Callable, Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

__all__ = [
    "RetrieveObjectByIDSerializerField", "WritableSerializerMethodField"
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
