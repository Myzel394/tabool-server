from apps.django.authentication.user.serializers import DetailStudentSerializer
from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseSubmissionSerializer

__all__ = [
    "StudentDetailSubmissionSerializer", "TeacherDetailSubmissionSerializer"
]


class StudentDetailSubmissionSerializer(BaseSubmissionSerializer):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "file", "name", "created_at", "id"
        ]
    
    lesson = StudentDetailLessonSerializer()


class TeacherDetailSubmissionSerializer(BaseSubmissionSerializer):
    class Meta(BaseSubmissionSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "publish_datetime", "file", "name", "associated_user", "id"
        ]
    
    lesson = TeacherDetailLessonSerializer()
    student = DetailStudentSerializer()
