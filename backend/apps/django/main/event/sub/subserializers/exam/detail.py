from apps.django.main.course.sub.subserializers.course import (
    StudentDetailCourseSerializer,
    TeacherDetailCourseSerializer,
)
from .base import BaseExamSerializer

__all__ = [
    "StudentDetailExamSerializer", "TeacherDetailExamSerializer"
]


class StudentDetailExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta):
        fields = [
            "course", "date", "title", "information", "id"
        ]
    
    course = StudentDetailCourseSerializer()


class TeacherDetailExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta):
        fields = [
            "course", "date", "title", "created_at", "information", "id"
        ]
    
    course = TeacherDetailCourseSerializer()
