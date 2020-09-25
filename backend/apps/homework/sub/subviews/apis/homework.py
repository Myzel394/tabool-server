from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from ...subserializers import HomeworkDetailSerializer, HomeworkListSerializer
from ....filters import HomeworkFilterSet
from ....models import Homework

__all__ = [
    "HomeworkViewSet"
]


class HomeworkViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HomeworkFilterSet
    search_fields = ["information"]
    ordering_fields = ["completed", "due_date"]
    
    def get_queryset(self):
        return Homework.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return HomeworkListSerializer
        return HomeworkDetailSerializer
