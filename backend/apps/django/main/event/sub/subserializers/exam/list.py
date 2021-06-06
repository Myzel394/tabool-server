from apps.django.main.course.sub.subserializers.course import (
    StudentDetailCourseSerializer,
    TeacherDetailCourseSerializer,
)
from .base import BaseExamSerializer

__all__ = [
    "StudentListExamSerializer", "TeacherListExamSerializer"
]


class StudentListExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta):
        fields = [
            "course", "date", "title", "id"
        ]

    course = StudentDetailCourseSerializer()


class TeacherListExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta):
        fields = [
            "course", "date", "title", "id"
        ]

    course = TeacherDetailCourseSerializer()
