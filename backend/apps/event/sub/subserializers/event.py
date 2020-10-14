from apps.school_data.public.serializer_fields import RoomField
from apps.utils.serializers import RandomIDSerializerMixin, UserRelationField
from .user_relations import UserEventRelationSerializer
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
            "room", "title", "start_datetime", "end_datetime", "id", "user_relation"
        ]
        read_only_fields = [
            "user_relation", "id"
        ]
    
    user_relation = UserRelationField(UserEventRelationSerializer)
    
    room = RoomField(required=False)
