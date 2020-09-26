from rest_framework import viewsets

from apps.utils.viewsets.mixins import RetrieveAllMixin
from ....models import Teacher
from ....serializers import TeacherDetailSerializer

__all__ = [
    "TeacherViewSet"
]


class TeacherViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    serializer_class = TeacherDetailSerializer
    model = Teacher
