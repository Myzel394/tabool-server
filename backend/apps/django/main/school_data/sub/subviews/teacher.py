from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.django.utils.viewsets import RetrieveAllMixin
from ...models import Teacher
from ...paginations import LargeSetPagination
from ...serializers import TeacherDetailSerializer, TeacherListSerializer

__all__ = [
    "TeacherViewSet"
]


class TeacherViewSet(viewsets.mixins.ListModelMixin, RetrieveAllMixin):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["first_name", "last_name", "short_name"]
    model = Teacher
    pagination_class = LargeSetPagination
    permission_classes = [IsAuthenticated]  # Teachers must be collected for full registration
    ordering_fields = ["first_name", "last_name", "short_name"]
    
    def get_serializer_class(self):
        if self.action == "list":
            return TeacherListSerializer
        return TeacherDetailSerializer
