from apps.django.authentication.user.serializers import (
    DetailTeacherSerializer,
)
from apps.django.authentication.user.sub.subserializers.student import DetailStudentSerializer
from .base import BaseCourseSerializer, ParticipantsCountMixin, WeekdaysMixin
from ..room import DetailRoomSerializer
from ..subject import DetailSubjectSerializer

__all__ = [
    "StudentDetailCourseSerializer", "TeacherDetailCourseSerializer"
]


class StudentDetailCourseSerializer(BaseCourseSerializer, ParticipantsCountMixin, WeekdaysMixin):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants_count", "subject", "teacher", "room", "weekdays", "id"
        ]
    
    subject = DetailSubjectSerializer()
    teacher = DetailTeacherSerializer()
    room = DetailRoomSerializer()


class TeacherDetailCourseSerializer(BaseCourseSerializer, WeekdaysMixin):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants", "subject", "teacher", "room", "weekdays", "id"
        ]
    
    subject = DetailSubjectSerializer()
    teacher = DetailTeacherSerializer()
    room = DetailRoomSerializer()
    participants = DetailStudentSerializer(many=True)
