from apps.django.main.course.sub.subserializers.course import (
    StudentDetailCourseSerializer,
    TeacherDetailCourseSerializer,
)
from .base import BaseLessonSerializer

__all__ = [
    "StudentDetailLessonSerializer", "TeacherDetailLessonSerializer"
]


class StudentDetailLessonSerializer(BaseLessonSerializer):
    class Meta(BaseLessonSerializer.Meta):
        fields = [
            "course", "start_hour", "end_hour", "weekday", "id"
        ]
    
    course = StudentDetailCourseSerializer()


class TeacherDetailLessonSerializer(BaseLessonSerializer):
    class Meta(BaseLessonSerializer.Meta):
        fields = [
            "course", "start_hour", "end_hour", "weekday", "id"
        ]
    
    course = TeacherDetailCourseSerializer()
