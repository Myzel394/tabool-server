from typing import *

from apps.django.authentication.user.serializers import (
    DetailTeacherSerializer,
)
from apps.django.authentication.user.sub.subserializers.student import DetailStudentSerializer
from .base import BaseCourseSerializer, ParticipantsCountMixin
from ..room import DetailRoomSerializer
from ..subject import DetailSubjectSerializer

if TYPE_CHECKING:
    pass

__all__ = [
    "StudentDetailCourseSerializer", "TeacherDetailCourseSerializer"
]


class StudentDetailCourseSerializer(BaseCourseSerializer, ParticipantsCountMixin):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants_count", "subject", "teacher", "room", "id"
        ]
    
    subject = DetailSubjectSerializer()
    teacher = DetailTeacherSerializer()
    room = DetailRoomSerializer()


class TeacherDetailCourseSerializer(BaseCourseSerializer):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants", "subject", "teacher", "room", "id"
        ]
    
    subject = DetailSubjectSerializer()
    teacher = DetailTeacherSerializer()
    room = DetailRoomSerializer()
    participants = DetailStudentSerializer(many=True)
