from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from ...subserializers import UserHomeworkDetailSerializer, UserHomeworkListSerializer
from ....models import UserHomework
from ....filters import HomeworkFilterSet

__all__ = [
    "UserHomeworkViewSet"
]


class UserHomeworkViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeworkFilterSet
    
    def get_queryset(self):
        return UserHomework.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action in ["list", "subject"]:
            return UserHomeworkListSerializer
        return UserHomeworkDetailSerializer

# TODO: Add AddUserHomeworkBySubjectViewSet!
