from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseClassbookSerializer

__all__ = [
    "StudentDetailClassbookSerializer", "TeacherDetailClassbookSerializer"
]


class StudentDetailClassbookSerializer(BaseClassbookSerializer):
    class Meta(BaseClassbookSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "presence_content", "online_content", "video_conference_link", "id"
        ]

    lesson = StudentDetailLessonSerializer()


class TeacherDetailClassbookSerializer(BaseClassbookSerializer):
    class Meta(BaseClassbookSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "presence_content", "online_content", "video_conference_link", "id"
        ]

    lesson = TeacherDetailLessonSerializer()
