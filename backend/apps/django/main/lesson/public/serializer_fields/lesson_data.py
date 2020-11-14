from apps.django.main.lesson.models import LessonData
from apps.django.main.lesson.sub.subserializers.lesson_data import LessonDataDetailSerializer
from apps.django.utils.serializers import WritableFromUserFieldMixin

__all__ = [
    "LessonDataField"
]


class LessonDataField(WritableFromUserFieldMixin):
    model = LessonData
    detail_serializer = LessonDataDetailSerializer
