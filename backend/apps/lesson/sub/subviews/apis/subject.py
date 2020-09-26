from rest_framework import viewsets

from apps.utils.viewsets.mixins import RetrieveAllMixin
from ....models import Subject
from ....serializers import SubjectDetailSerializer

__all__ = [
    "SubjectViewSet"
]


class SubjectViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    serializer_class = SubjectDetailSerializer
    model = Subject
