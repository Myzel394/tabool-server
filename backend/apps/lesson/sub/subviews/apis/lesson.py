from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.utils.viewsets import RetrieveFromUserMixin
from ....filters import LessonFilterSet
from ....models import Lesson
from ....paginations import LessonPagination
from ....serializers import LessonDetailSerializer, LessonListSerializer

__all__ = [
    "LessonViewSet"
]


class LessonViewSet(viewsets.mixins.ListModelMixin, RetrieveFromUserMixin):
    model = Lesson
    pagination_class = LessonPagination
    filterset_class = LessonFilterSet
    filter_backends = [DjangoFilterBackend]
    
    def get_serializer_class(self):
        if self.action == "list":
            return LessonListSerializer
        return LessonDetailSerializer
