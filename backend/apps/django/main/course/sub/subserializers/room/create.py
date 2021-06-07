from rest_framework import serializers

from .base import BaseRoomSerializer
from ....validators import does_room_exist

__all__ = [
    "CreateRoomSerializer"
]


class CreateRoomSerializer(BaseRoomSerializer):
    class Meta(BaseRoomSerializer.Meta):
        fields = [
            "place"
        ]

    place = serializers.CharField(
        validators=[does_room_exist],
    )
