from typing import *

from rest_framework import serializers

__all__ = [
    "UserRelationSerializerField"
]


class UserRelationSerializerField(serializers.SerializerMethodField):
    def __init__(
            self,
            serializer_class: Type[serializers.ModelSerializer],
            setter_method_name: Optional[str] = None,
            *args,
            **kwargs
    ):
        self.setter_method_name = setter_method_name
        self.serializer_class = serializer_class
        
        kwargs.setdefault("read_only", False)
        read_only = kwargs.pop("read_only")
        
        kwargs['source'] = '*'
        super().__init__(*args, **kwargs)
        self.read_only = read_only
        self.instance = None
        self.user = None
    
    def get_object(self):
        return self.instance.user_relations.only("user").get(user=self.user)
    
    def bind(self, field_name: str, parent):
        data = super().bind(field_name, parent)
        self.setter_method_name = self.setter_method_name or f"set_{field_name}"
        self.instance = parent.instance
        
        if (key := "request") in parent.context:
            self.user = parent.context[key].user
        
        return data
    
    def to_representation(self, _):
        return self.serializer_class().to_representation(self.get_object())
    
    def to_internal_value(self, data):
        instance = self.serializer_class(instance=self.get_object(), data=data)
        instance.is_valid(raise_exception=True)
        
        return instance.save()
