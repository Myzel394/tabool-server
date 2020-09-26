from rest_framework import serializers

__all__ = [
    "DefaultAccessSerializer"
]


class DefaultAccessSerializer(serializers.Serializer):
    id = serializers.CharField(
        allow_blank=False,
    )
