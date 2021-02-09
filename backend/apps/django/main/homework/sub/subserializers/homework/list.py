from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseHomeworkSerializer, TruncatedInformationSerializer

__all__ = [
    "StudentListHomeworkSerializer", "TeacherListHomeworkSerializer"
]


class StudentListHomeworkSerializer(BaseHomeworkSerializer, TruncatedInformationSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "due_date", "id", "truncated_information",
        ]
    
    lesson = StudentDetailLessonSerializer()


class TeacherListHomeworkSerializer(BaseHomeworkSerializer, TruncatedInformationSerializer):
    class Meta(BaseHomeworkSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "due_date", "id", "truncated_information",
        ]
    
    lesson = TeacherDetailLessonSerializer()
