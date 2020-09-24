from rest_framework import viewsets

from .mixins import HomeworkBySubjectMixin
from ....models import TeacherHomework
from ....serializers import TeacherHomeworkDetailSerializer, TeacherHomeworkListSerializer

__all__ = [
    "TeacherHomeworkViewSet"
]


class TeacherHomeworkViewSet(
    viewsets.ReadOnlyModelViewSet,
    HomeworkBySubjectMixin
):
    def get_queryset(self):
        return TeacherHomework.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action in ["list", "by_subject"]:
            return TeacherHomeworkListSerializer
        return TeacherHomeworkDetailSerializer
