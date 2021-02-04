from rest_framework import serializers

from ....models import Room

__all__ = [
    "BaseRoomSerializer"
]


class BaseRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
