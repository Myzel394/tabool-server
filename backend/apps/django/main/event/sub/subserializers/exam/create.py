from apps.django.main.lesson.public.serializer_fields.course import CourseField
from apps.django.main.school_data.public.serializer_fields.room import RoomField
from .base import BaseExamSerializer

__all__ = [
    "CreateExamSerializer"
]


class CreateExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta):
        fields = [
            "course", "room", "targeted_date", "information"
        ]
    
    course = CourseField(detail=True)
    room = RoomField(required=False, detail=True)
