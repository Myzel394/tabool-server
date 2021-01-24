from django_filters.rest_framework import DjangoFilterBackend
from django_hint import RequestType
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.django.utils.viewsets import RetrieveFromUserMixin
from ....filters import LessonFilterSet
from ....models import Lesson, LessonData
from ....paginations import LessonPagination
from ....serializers import DetailLessonSerializer, ListLessonDataSerializer, ListLessonSerializer

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
            return ListLessonSerializer
        return DetailLessonSerializer
    
    @action(detail=False, methods=["GET"], url_path="lesson-data")
    def lesson_data_list(self, request: RequestType):
        lesson_data = LessonData.objects.from_user(request.user)
        
        return ListLessonDataSerializer(lesson_data, many=True).data
