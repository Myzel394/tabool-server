from apps.django.main.timetable.sub.subserializers.lesson import DetailLessonSerializer
from .base import BaseClassbookSerializer

__all__ = [
    "DetailClassbookSerializer"
]


class DetailClassbookSerializer(BaseClassbookSerializer):
    class Meta(BaseClassbookSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "presence_content", "online_content", "id"
        ]
    
    lesson = DetailLessonSerializer()
