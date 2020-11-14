from apps.django.main.lesson.models import Course
from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...sub.subserializers.course import CourseDetailSerializer

__all__ = [
    "CourseField"
]


class CourseField(WritableFromUserFieldMixin):
    model = Course
    detail_serializer = CourseDetailSerializer
