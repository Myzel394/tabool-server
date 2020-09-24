from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from ...subserializers import UserHomeworkDetailSerializer, UserHomeworkListSerializer
from ....filters import UserHomeworkFilterSet
from ....models import UserHomework

__all__ = [
    "UserHomeworkViewSet"
]


class UserHomeworkViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserHomeworkFilterSet
    search_fields = ["information"]
    ordering_fields = ["completed", "due_date"]
    
    def get_queryset(self):
        return UserHomework.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return UserHomeworkListSerializer
        return UserHomeworkDetailSerializer
