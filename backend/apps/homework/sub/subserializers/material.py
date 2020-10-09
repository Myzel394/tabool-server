from apps.utils.serializers import RandomIDSerializerMixin

from ...models import Material

__all__ = [
    "MaterialDetailSerializer"
]


class MaterialDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Material
        fields = [
            "file", "name", "added_at", "id"
        ]
