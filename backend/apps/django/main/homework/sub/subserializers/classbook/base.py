from rest_framework import serializers

from ....models import Classbook

__all__ = [
    "BaseClassbookSerializer"
]


class BaseClassbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classbook
