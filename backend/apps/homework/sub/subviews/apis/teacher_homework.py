from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ....models import TeacherHomework
from ....serializers import TeacherHomeworkDetailSerializer, TeacherHomeworkListSerializer

__all__ = [
    "TeacherHomeworkViewSet"
]


class TeacherHomeworkViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return TeacherHomework.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return TeacherHomeworkListSerializer
        return TeacherHomeworkDetailSerializer
