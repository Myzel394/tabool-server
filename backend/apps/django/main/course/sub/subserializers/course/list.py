from .base import BaseCourseSerializer, ParticipantsCountMixin
from ..subject import DetailSubjectSerializer

__all__ = [
    "ListCourseSerializer",
]


class ListCourseSerializer(BaseCourseSerializer, ParticipantsCountMixin):
    class Meta(BaseCourseSerializer.Meta):
        fields = [
            "course_number", "participants_count", "subject", "id"
        ]
    
    subject = DetailSubjectSerializer()
