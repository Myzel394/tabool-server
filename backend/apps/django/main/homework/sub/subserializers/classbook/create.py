from apps.django.main.timetable.public.serializer_fields.lesson import LessonField
from .base import BaseClassbookSerializer

__all__ = [
    "CreateClassbookSerializer"
]


class CreateClassbookSerializer(BaseClassbookSerializer):
    class Meta(BaseClassbookSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "presence_content", "online_content"
        ]
    
    lesson = LessonField()
