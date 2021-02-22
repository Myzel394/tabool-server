from rest_framework import serializers

from ....models import Material

__all__ = [
    "BaseMaterialSerializer", "SizeMaterialMixin"
]


class BaseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material


class SizeMaterialMixin(serializers.Serializer):
    size = serializers.SerializerMethodField()
    
    def get_size(self, instance: Material) -> int:
        return instance.file.size
