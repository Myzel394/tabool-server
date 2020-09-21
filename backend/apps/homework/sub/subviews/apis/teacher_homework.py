from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ....models import TeacherHomework
from ....serializers import TeacherHomeworkSerializer

__all__ = [
    "TeacherHomeworkViewSet"
]


class TeacherHomeworkViewSet(viewsets.ReadOnlyModelViewSet):
    """Returns homeworks based on lessons"""
    serializer_class = TeacherHomeworkSerializer
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return TeacherHomework.objects.from_user(self.request.user)
