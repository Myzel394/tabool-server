from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ...subserializers import UserHomeworkDetailSerializer, UserHomeworkListSerializer
from ....models import UserHomework

__all__ = [
    "UserHomeworkViewSet"
]


class UserHomeworkViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return UserHomework.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return UserHomeworkListSerializer
        return UserHomeworkDetailSerializer
