from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.django.utils.viewsets import RetrieveAllMixin
from ...models import Teacher
from ...paginations import LargeSetPagination
from ...serializers import TeacherDetailSerializer, TeacherListSerializer

__all__ = [
    "TeacherViewSet"
]


class TeacherViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "short_name"]
    model = Teacher
    pagination_class = LargeSetPagination
    
    def get_serializer_class(self):
        if self.action == "list":
            return TeacherListSerializer
        return TeacherDetailSerializer
