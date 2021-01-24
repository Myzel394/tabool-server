from apps.django.main.school_data.public.serializer_fields.room import RoomField
from .base import BaseLessonDataSerializer
from ....models import LessonData
from ....public.serializer_fields.course import CourseField

__all__ = [
    "DetailLessonDataSerializer"
]


class DetailLessonDataSerializer(BaseLessonDataSerializer):
    class Meta(BaseLessonDataSerializer.Meta):
        model = LessonData
        fields = [
            "room", "course", "start_time", "end_time", "weekday", "id"
        ]
    
    course = CourseField(detail=True)
    room = RoomField(required=False, detail=True)
