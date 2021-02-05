from apps.django.main.timetable.public.serializer_fields.lesson import LessonField
from .base import BaseSubmissionSerializer

__all__ = [
    "CreateSubmissionSerializer"
]


class CreateSubmissionSerializer(BaseSubmissionSerializer):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "file"
        ]
    
    lesson = LessonField()
