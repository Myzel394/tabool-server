from apps.django.main.timetable.public.serializer_fields.lesson import LessonField
from .base import BaseMaterialSerializer

__all__ = [
    "CreateMaterialSerializer"
]


class CreateMaterialSerializer(BaseMaterialSerializer):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "announce", "file", "name"
        ]
    
    lesson = LessonField()
