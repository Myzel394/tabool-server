from apps.django.main.timetable.sub.subserializers.lesson import DetailLessonSerializer
from .base import BaseMaterialSerializer

__all__ = [
    "DetailMaterialSerializer"
]


class DetailMaterialSerializer(BaseMaterialSerializer):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "announce", "created_at", "file", "id"
        ]
    
    lesson = DetailLessonSerializer()
