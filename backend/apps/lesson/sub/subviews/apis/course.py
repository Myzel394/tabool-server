from apps.utils.viewsets.mixins import RetrieveFromUserMixin
from ....models import Course
from ....serializers import CourseDetailSerializer

__all__ = [
    "CourseViewSet"
]


class CourseViewSet(RetrieveFromUserMixin):
    serializer_class = CourseDetailSerializer
    model = Course
