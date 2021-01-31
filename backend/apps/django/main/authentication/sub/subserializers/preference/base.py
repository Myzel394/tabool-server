from rest_framework import serializers

from ....models import Preference

__all__ = [
    "BasePreferenceSerializer"
]


class BasePreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
