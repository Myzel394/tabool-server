from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from apps.django.utils.viewsets import RetrieveFromUserMixin
from ....models import Course
from ....serializers import DetailCourseSerializer, ListCourseSerializer

__all__ = [
    "CourseViewSet"
]


class CourseViewSet(viewsets.mixins.ListModelMixin, RetrieveFromUserMixin):
    filter_backends = [SearchFilter]
    search_fields = ["subject__name", "course_number", "teacher__last_name"]
    model = Course
    
    def get_serializer_class(self):
        if self.action in ["list"]:
            return ListCourseSerializer
        return DetailCourseSerializer
