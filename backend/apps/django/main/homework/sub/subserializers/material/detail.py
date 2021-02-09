from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseMaterialSerializer

__all__ = [
    "StudentDetailMaterialSerializer", "TeacherDetailMaterialSerializer"
]


class StudentDetailMaterialSerializer(BaseMaterialSerializer):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "announce", "name", "created_at", "file", "id"
        ]
    
    lesson = StudentDetailLessonSerializer()


class TeacherDetailMaterialSerializer(BaseMaterialSerializer):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "announce", "name", "created_at", "file", "id"
        ]
    
    lesson = TeacherDetailLessonSerializer()
