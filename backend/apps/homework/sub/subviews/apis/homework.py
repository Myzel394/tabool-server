from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from ....filters import HomeworkFilterSet
from ....models import Homework
from ....serializers import HomeworkDetailSerializer, HomeworkListSerializer

__all__ = [
    "HomeworkViewSet"
]


class HomeworkViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HomeworkFilterSet
    search_fields = ["information"]
    ordering_fields = ["completed", "due_date"]
    
    def get_queryset(self):
        return Homework.objects.from_user(self.request.user).distinct()
    
    def get_serializer_class(self):
        if self.action == "list":
            return HomeworkListSerializer
        return HomeworkDetailSerializer
