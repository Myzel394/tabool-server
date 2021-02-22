from apps.django.authentication.user.serializers import DetailStudentSerializer
from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseSubmissionSerializer, SizeMixin

__all__ = [
    "StudentDetailSubmissionSerializer", "TeacherDetailSubmissionSerializer"
]


class StudentDetailSubmissionSerializer(BaseSubmissionSerializer, SizeMixin):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "file", "name", "created_at", "size", "id"
        ]
    
    lesson = StudentDetailLessonSerializer()


class TeacherDetailSubmissionSerializer(BaseSubmissionSerializer, SizeMixin):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "file", "name", "student", "size", "id"
        ]
    
    lesson = TeacherDetailLessonSerializer()
    student = DetailStudentSerializer()
