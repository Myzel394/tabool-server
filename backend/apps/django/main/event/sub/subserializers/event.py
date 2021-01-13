from apps.django.main.school_data.public.serializer_fields.room import RoomField
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin, UserRelationField
from .user_relations import UserEventRelationSerializer
from ...models import Event

__all__ = [
    "EventListSerializer", "EventDetailSerializer"
]


class EventListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "event"
    
    class Meta:
        model = Event
        fields = [
            "title", "start_datetime", "end_datetime", "id"
        ]


class EventDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "event"
    
    class Meta:
        model = Event
        fields = [
            "room", "title", "start_datetime", "end_datetime", "id", "user_relation"
        ]
        read_only_fields = [
            "user_relation", "id"
        ]
    
    user_relation = UserRelationField(
        UserEventRelationSerializer,
        default={
            "ignore": False
        }
    )
    
    room = RoomField(required=False, detail=True)
