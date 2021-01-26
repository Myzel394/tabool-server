from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.django.main.event.models import Exam
from apps.django.utils.viewsets import DetailSerializerViewSetMixin
from ....filters import ExamFilterSet
from ....serializers import CreateExamSerializer, DetailExamSerializer, ListExamSerializer, UpdateExamSerializer

__all__ = [
    "ExamViewSet"
]


class ExamViewSet(
    DetailSerializerViewSetMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.mixins.ListModelMixin,
):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExamFilterSet
    search_fields = ["information"]
    ordering_fields = ["targeted_date"]
    detail_serializer = DetailExamSerializer
    serializer_action_map = {
        "create": CreateExamSerializer,
        "update": UpdateExamSerializer,
        "partial_update": UpdateExamSerializer,
        "list": ListExamSerializer,
        "retrieve": DetailExamSerializer
    }
    
    def get_queryset(self):
        return Exam.objects.from_user(self.request.user)
