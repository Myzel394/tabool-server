from apps.django.utils.viewsets import RetrieveFromUserMixin
from ....models import Course
from ....serializers import CourseDetailSerializer

__all__ = [
    "CourseViewSet"
]


class CourseViewSet(RetrieveFromUserMixin):
    serializer_class = CourseDetailSerializer
    model = Course
