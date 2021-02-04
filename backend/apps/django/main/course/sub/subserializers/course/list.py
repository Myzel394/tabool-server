from .base import BaseCourseSerializer, ParticipantsCountMixin
from ..subject import DetailSubjectSerializer

__all__ = [
    "StudentListCourseSerializer", "TeacherListCourseSerializer"
]


class StudentListCourseSerializer(BaseCourseSerializer, ParticipantsCountMixin):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants_count", "subject", "id"
        ]
    
    subject = DetailSubjectSerializer()


class TeacherListCourseSerializer(BaseCourseSerializer, ParticipantsCountMixin):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants_count", "subject", "id"
        ]
    
    subject = DetailSubjectSerializer()
