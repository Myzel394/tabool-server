from apps.django.main.school_data.public.serializer_fields.room import RoomField
from apps.django.utils.serializers import UserRelationField
from .base import BaseEventSerializer
from ..user_relations import UserEventRelationSerializer

__all__ = [
    "DetailEventSerializer"
]


class DetailEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        fields = [
            "room", "title", "start_datetime", "end_datetime", "id", "user_relation"
        ]
    
    user_relation = UserRelationField(
        UserEventRelationSerializer,
        default={
            "ignore": False
        }
    )
    
    room = RoomField(detail=True)
