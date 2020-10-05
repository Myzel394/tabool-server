from apps.lesson.public.serializer_fields import RoomField
from apps.relation_managers.serializers import UserRelationSerializerField
from apps.utils.serializers import RandomIDSerializerMixin
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
    
    user_relation = UserRelationSerializerField(serializer_class=UserEventRelationSerializer)
    
    room = RoomField(required=False)
