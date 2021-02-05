from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Course

__all__ = [
    "CourseField"
]


class CourseField(WritableFromUserFieldMixin):
    model = Course
