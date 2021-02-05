from rest_framework import serializers

from ....models import Material

__all__ = [
    "BaseMaterialSerializer"
]


class BaseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
