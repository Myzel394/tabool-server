from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ....models import UserHomework
from ....serializers import UserHomeworkSerializer

__all__ = [
    "UserHomeworkViewSet"
]


class UserHomeworkViewSet(viewsets.ModelViewSet):
    serializer_class = UserHomeworkSerializer
    permission_classes = [
        IsAuthenticated
    ]
    
    def get_queryset(self):
        return UserHomework.objects.from_user(self.request.user)
