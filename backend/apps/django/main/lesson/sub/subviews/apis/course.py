from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.django.utils.viewsets import RetrieveFromUserMixin
from ....models import Course
from ....serializers import CourseDetailSerializer

__all__ = [
    "CourseViewSet"
]


class CourseViewSet(viewsets.mixins.ListModelMixin, RetrieveFromUserMixin):
    filter_backends = [SearchFilter]
    search_fields = ["subject__name", "course_number", "teacher__lastname"]
    serializer_class = CourseDetailSerializer
    model = Course
