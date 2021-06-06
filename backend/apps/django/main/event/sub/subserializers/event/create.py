from apps.django.main.course.public.serializer_fields.room import RoomField
from .base import BaseEventSerializer

__all__ = [
    "CreateEventSerializer"
]


class CreateEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        fields = [
            "room", "title", "start_datetime", "end_datetime"
        ]

    room = RoomField()
