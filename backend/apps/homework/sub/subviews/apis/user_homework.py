from rest_framework import viewsets
from rest_framework.decorators import action

from .mixins import HomeworkBySubjectMixin
from ...subserializers import UserHomeworkDetailSerializer, UserHomeworkListSerializer
from ....models import UserHomework

__all__ = [
    "UserHomeworkViewSet"
]


class UserHomeworkViewSet(
    viewsets.ModelViewSet,
    HomeworkBySubjectMixin,
):
    def get_queryset(self):
        return UserHomework.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action in ["list", "by_subject"]:
            return UserHomeworkListSerializer
        return UserHomeworkDetailSerializer

# TODO: Add AddUserHomeworkBySubjectViewSet!
