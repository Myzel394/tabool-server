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
            "name", "added_at", "id", "size"
        ]
    
    size = serializers.SerializerMethodField()
    
    def get_size(self, instance: Material) -> int:
        return instance.file.size
