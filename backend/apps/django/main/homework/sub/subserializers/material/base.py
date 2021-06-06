from rest_framework import serializers

from apps.django.utils.serializers import ValidationSerializer
from ....models import Material

__all__ = [
    "BaseMaterialSerializer", "MaterialSizeSerializerMixin"
]


class BaseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material


class MaterialSizeSerializerMixin(ValidationSerializer):
    size = serializers.ReadOnlyField(source="file.size")
