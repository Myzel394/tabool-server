from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from apps.event.models import Classtest
from ....filters import ClasstestFilterSet
from ....serializers import ClasstestDetailSerializer, ClasstestListSerializer

__all__ = [
    "ClasstestViewSet"
]


class ClasstestViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ClasstestFilterSet
    search_fields = ["information"]
    ordering_fields = ["targeted_date"]
    
    def get_queryset(self):
        return Classtest.objects.from_queryset(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return ClasstestListSerializer
        return ClasstestDetailSerializer
