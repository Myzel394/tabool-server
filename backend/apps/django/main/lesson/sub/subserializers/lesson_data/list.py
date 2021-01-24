from .base import BaseLessonDataSerializer
from ....public.serializer_fields.course import CourseField

__all__ = [
    "ListLessonDataSerializer"
]


class ListLessonDataSerializer(BaseLessonDataSerializer):
    class Meta(BaseLessonDataSerializer.Meta):
        fields = [
            "course", "start_time", "end_time", "weekday", "id"
        ]
    
    course = CourseField()
