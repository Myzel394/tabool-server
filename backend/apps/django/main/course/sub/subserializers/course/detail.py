from apps.django.authentication.user.serializers import (
    DetailTeacherSerializer, DetailUserSerializer,
)
from .base import BaseCourseSerializer, ParticipantsCountMixin
from ..subject import DetailSubjectSerializer

__all__ = [
    "StudentDetailCourseSerializer", "TeacherDetailCourseSerializer"
]


class StudentDetailCourseSerializer(BaseCourseSerializer, ParticipantsCountMixin):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants_count", "subject", "teacher", "id"
        ]
    
    subject = DetailSubjectSerializer()
    teacher = DetailTeacherSerializer()


class TeacherDetailCourseSerializer(BaseCourseSerializer):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants", "subject", "teacher", "id"
        ]
    
    subject = DetailSubjectSerializer()
    teacher = DetailTeacherSerializer()
    participants = DetailUserSerializer(many=True)