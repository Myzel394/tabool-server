from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from apps.lesson.sub.subserializers import RoomDetailSerializer
from ...models import Event

__all__ = [
    "EventListSerializer", "EventDetailSerializer"
]


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title", "start_datetime", "end_datetime", "id"
        ]


class EventDetailSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Event
        fields = [
            "room", "title", "start_datetime", "end_datetime", "id"
        ]
    
    room = RoomDetailSerializer()
