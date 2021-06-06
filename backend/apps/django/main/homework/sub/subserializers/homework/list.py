from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseHomeworkSerializer, TruncatedInformationSerializerMixin

__all__ = [
    "StudentListHomeworkSerializer", "TeacherListHomeworkSerializer"
]


class StudentListHomeworkSerializer(BaseHomeworkSerializer, TruncatedInformationSerializerMixin):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "due_date", "id", "truncated_information",
        ]
    
    lesson = StudentDetailLessonSerializer()


class TeacherListHomeworkSerializer(BaseHomeworkSerializer, TruncatedInformationSerializerMixin):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "due_date", "id", "truncated_information",
        ]
    
    lesson = TeacherDetailLessonSerializer()
