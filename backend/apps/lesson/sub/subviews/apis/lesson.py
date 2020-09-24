from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import viewsets

from ....filters import LessonFilterSet
from ....models import Lesson
from ....serializers import LessonDetailSerializer, LessonListSerializer

__all__ = [
    "LessonViewSet"
]


class LessonViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LessonFilterSet
    ordering_fields = ["date", "attendance"]
    
    def get_queryset(self):
        return Lesson.objects.from_user(self.request.user)
    
    def get_serializer_class(self):
        if self.action == "list":
            return LessonListSerializer
        return LessonDetailSerializer
