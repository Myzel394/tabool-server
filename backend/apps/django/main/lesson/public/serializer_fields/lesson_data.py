from apps.django.utils.serializers import WritableFromUserFieldMixin
from ...models import LessonData
from ...sub.subserializers.lesson_data.detail import DetailLessonDataSerializer

__all__ = [
    "LessonDataField"
]


class LessonDataField(WritableFromUserFieldMixin):
    model = LessonData
    detail_serializer = DetailLessonDataSerializer
