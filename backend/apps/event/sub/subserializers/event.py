from apps.lesson.public.serializer_fields import RoomField
from apps.utils.serializers import RandomIDSerializerMixin, UserRelationSerializerMixin, WritableSerializerMethodField
from ...models import Event
from .user_relations import UserEventRelationSerializer

__all__ = [
    "EventListSerializer", "EventDetailSerializer"
]


class EventListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Event
        fields = [
            "title", "start_datetime", "end_datetime", "id"
        ]


class EventDetailSerializer(UserRelationSerializerMixin, RandomIDSerializerMixin):
    class Meta:
        model = Event
        fields = [
            "room", "title", "start_datetime", "end_datetime", "id", "user_relation"
        ]
    
    user_relation = WritableSerializerMethodField(deserializer_field=UserEventRelationSerializer())
    
    room = RoomField(required=False)
