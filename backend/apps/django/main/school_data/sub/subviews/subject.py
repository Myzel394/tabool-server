from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.utils.viewsets import RetrieveAllMixin
from ...models import Subject
from ...paginations import LargeSetPagination
from ...serializers import SubjectSerializer

__all__ = [
    "SubjectViewSet"
]


class SubjectViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    serializer_class = SubjectSerializer
    model = Subject
    pagination_class = LargeSetPagination
    ordering_fields = ["name", "short_name"]
