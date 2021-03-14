from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.utils.viewsets import RetrieveFromUserMixin
from ....models import Subject
from ....serializers import DetailSubjectSerializer

__all__ = [
    "SubjectViewSet"
]


class SubjectViewSet(
    viewsets.mixins.ListModelMixin,
    RetrieveFromUserMixin
):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    serializer_class = DetailSubjectSerializer
    model = Subject
    ordering_fields = ["name", "short_name"]
