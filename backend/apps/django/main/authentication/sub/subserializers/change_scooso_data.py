from rest_framework import serializers

__all__ = [
    "ScoosoChangeSerializer"
]


class ScoosoChangeSerializer(serializers.Serializer):
    username = serializers.CharField(
        min_length=1
    )
    password = serializers.CharField(
        min_length=1
    )
