from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.utils.viewsets.mixins import RetrieveAllMixin
from ...subpaginations import LargeSetPagination
from ....models import Teacher
from ....serializers import TeacherDetailSerializer

__all__ = [
    "TeacherViewSet"
]


class TeacherViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "short_name"]
    serializer_class = TeacherDetailSerializer
    model = Teacher
    pagination_class = LargeSetPagination
