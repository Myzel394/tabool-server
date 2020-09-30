from rest_framework import serializers

from apps.lesson.models import RoomScoosoData
from apps.lesson.public.serializer_fields import RoomField

__all__ = [
    "RoomScoosoDataSerializer"
]


class RoomScoosoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomScoosoData
        fields = [
            "place", "scooso_id", "room"
        ]
    
    room = RoomField()

