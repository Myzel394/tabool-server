from rest_framework import serializers

from ....models import User

__all__ = [
    "BaseUserSerializer"
]


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
