from rest_framework import serializers

from .base import BasePreferenceSerializer

__all__ = [
    "UpdatePreferenceSerializer"
]


class UpdatePreferenceSerializer(BasePreferenceSerializer):
    class Meta(BasePreferenceSerializer.Meta):
        fields = [
            "data"
        ]
    
    data = serializers.JSONField()
