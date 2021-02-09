from apps.django.authentication.user.sub.subserializers.teacher import DetailTeacherSerializer
from apps.django.main.course.sub.subserializers.room import DetailRoomSerializer
from apps.django.main.course.sub.subserializers.subject import DetailSubjectSerializer
from apps.django.main.timetable.sub.subserializers.lesson import (
    StudentDetailLessonSerializer,
    TeacherDetailLessonSerializer,
)
from .base import BaseModificationSerializer

__all__ = [
    "StudentDetailModificationSerializer", "TeacherDetailModificationSerializer"
]


class StudentDetailModificationSerializer(BaseModificationSerializer):
    class Meta(BaseModificationSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "new_room", "new_subject", "new_teacher", "information", "modification_type", "id"
        ]
    
    new_room = DetailRoomSerializer()
    new_subject = DetailSubjectSerializer()
    new_teacher = DetailTeacherSerializer()
    lesson = StudentDetailLessonSerializer()


class TeacherDetailModificationSerializer(BaseModificationSerializer):
    class Meta(BaseModificationSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "new_room", "new_subject", "new_teacher", "information", "modification_type", "id"
        ]
    
    new_room = DetailRoomSerializer()
    new_subject = DetailSubjectSerializer()
    new_teacher = DetailTeacherSerializer()
    lesson = TeacherDetailLessonSerializer()
