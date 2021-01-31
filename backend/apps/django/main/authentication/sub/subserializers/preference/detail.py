from .base import BasePreferenceSerializer

__all__ = [
    "DetailPreferenceSerializer"
]


class DetailPreferenceSerializer(BasePreferenceSerializer):
    class Meta(BasePreferenceSerializer.Meta):
        fields = [
            "id", "data"
        ]
