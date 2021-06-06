from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseMaterialSerializer, MaterialSizeSerializerMixin

__all__ = [
    "StudentDetailMaterialSerializer", "TeacherDetailMaterialSerializer"
]


class StudentDetailMaterialSerializer(BaseMaterialSerializer, MaterialSizeSerializerMixin):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "name", "file", "size", "id"
        ]

    lesson = StudentDetailLessonSerializer()


class TeacherDetailMaterialSerializer(BaseMaterialSerializer, MaterialSizeSerializerMixin):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "announce", "name", "created_at", "file", "size", "id"
        ]

    lesson = TeacherDetailLessonSerializer()
