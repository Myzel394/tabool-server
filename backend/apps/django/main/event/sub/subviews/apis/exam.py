from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.main.event.models import Exam
from ....filters import ExamFilterSet
from ....serializers import ExamDetailSerializer, ExamListSerializer

__all__ = [
    "ExamViewSet"
]


class ExamViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExamFilterSet
    search_fields = ["information"]
    ordering_fields = ["targeted_date"]
    
    def get_queryset(self):
        return Exam.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return ExamListSerializer
        return ExamDetailSerializer
