from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Course
from ...sub.subserializers.course.detail import DetailCourseSerializer

__all__ = [
    "CourseField"
]


class CourseField(WritableFromUserFieldMixin):
    model = Course
    detail_serializer = DetailCourseSerializer
