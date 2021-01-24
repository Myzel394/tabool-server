from apps.django.main.school_data.public.serializer_fields.room import RoomField
from .base import BaseExamSerializer

__all__ = [
    "UpdateExamSerializer"
]


class UpdateExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta):
        fields = [
            "room", "targeted_date", "information"
        ]
    
    room = RoomField(required=False, detail=True)
