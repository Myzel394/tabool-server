from apps.lesson.public.serializer_fields import RoomField
from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Event

__all__ = [
    "EventListSerializer", "EventDetailSerializer"
]


class EventListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Event
        fields = [
            "title", "start_datetime", "end_datetime", "id"
        ]


class EventDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Event
        fields = [
            "room", "title", "start_datetime", "end_datetime", "id"
        ]
    
    room = RoomField(required=False)
