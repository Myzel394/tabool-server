from typing import *

from rest_framework import serializers

from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from ...models import Material

__all__ = [
    "MaterialDetailSerializer",
]


class MaterialDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "material"
    
    class Meta:
        model = Material
        fields = [
            "name", "added_at", "size", "id", "file", "is_deleted"
        ]
    
    size = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    
    def get_file(self, instance: Material) -> Optional[str]:
        if instance.file.name:
            return instance.file.url
        return None
    
    def get_size(self, instance: Material) -> Optional[int]:
        if instance.file.name:
            return instance.file.size
        return None
