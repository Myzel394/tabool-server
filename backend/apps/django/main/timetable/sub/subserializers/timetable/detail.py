from .base import BaseTimetableSerializer
from ..lesson import StudentDetailLessonSerializer

__all__ = [
    "StudentDetailTimetableSerializer"
]


class StudentDetailTimetableSerializer(BaseTimetableSerializer):
    class Meta(BaseTimetableSerializer.Meta):
        fields = [
            "lessons", "id"
        ]

    lessons = StudentDetailLessonSerializer(many=True)
