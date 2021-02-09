from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseModificationSerializer

__all__ = [
    "StudentListModificationSerializer", "TeacherListModificationSerializer"
]


class StudentListModificationSerializer(BaseModificationSerializer):
    class Meta(BaseModificationSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "modification_type"
        ]
    
    lesson = StudentDetailLessonSerializer()


class TeacherListModificationSerializer(BaseModificationSerializer):
    class Meta(BaseModificationSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "modification_type"
        ]
    
    lesson = TeacherDetailLessonSerializer()
