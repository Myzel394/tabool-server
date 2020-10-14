from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.utils.viewsets import RetrieveAllMixin
from ...models import Subject
from ...paginations import LargeSetPagination
from ...serializers import SubjectDetailSerializer

__all__ = [
    "SubjectViewSet"
]


class SubjectViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    serializer_class = SubjectDetailSerializer
    model = Subject
    pagination_class = LargeSetPagination
