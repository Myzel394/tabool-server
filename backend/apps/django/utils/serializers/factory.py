from typing import *

from rest_framework import serializers

__all__ = [
    "serializer_no_readonly_fields_factory"
]


def serializer_no_readonly_fields_factory(
        serializer_class: Type[serializers.Serializer]
) -> Type[serializers.Serializer]:
    class Factory(serializer_class):
        class Meta(serializer_class.Meta):
            fields = list(
                set(serializer_class.Meta.fields) - set(getattr(serializer_class.Meta, "read_only", []))
            )
            read_only = []
    
    return Factory
