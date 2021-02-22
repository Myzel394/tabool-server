from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseMaterialSerializer, SizeMaterialMixin

__all__ = [
    "StudentDetailMaterialSerializer", "TeacherDetailMaterialSerializer"
]


class StudentDetailMaterialSerializer(BaseMaterialSerializer, SizeMaterialMixin):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "name", "file", "size", "id"
        ]
    
    lesson = StudentDetailLessonSerializer()


class TeacherDetailMaterialSerializer(BaseMaterialSerializer, SizeMaterialMixin):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "announce", "name", "created_at", "file", "size", "id"
        ]
    
    lesson = TeacherDetailLessonSerializer()
