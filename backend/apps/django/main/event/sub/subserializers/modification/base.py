from rest_framework import serializers

from ....models import Modification

__all__ = [
    "BaseModificationSerializer"
]


class BaseModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modification
