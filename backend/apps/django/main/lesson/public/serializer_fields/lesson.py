from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import Lesson
from ...sub.subserializers.lesson.related_detail import RelatedDetailLessonSerializer

__all__ = [
    "LessonField"
]


class LessonField(WritableFromUserFieldMixin):
    model = Lesson
    detail_serializer = RelatedDetailLessonSerializer
