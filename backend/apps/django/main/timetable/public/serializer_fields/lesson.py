from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Lesson

__all__ = [
    "LessonField"
]


class LessonField(WritableFromUserFieldMixin):
    model = Lesson
