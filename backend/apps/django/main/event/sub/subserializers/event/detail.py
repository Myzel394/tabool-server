from apps.django.main.course.sub.subserializers.room import DetailRoomSerializer
from .base import BaseEventSerializer

__all__ = [
    "DetailEventSerializer"
]


class DetailEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        fields = [
            "room", "title", "start_datetime", "end_datetime", "information", "id"
        ]
    
    room = DetailRoomSerializer()
