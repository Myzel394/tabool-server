from apps.django.main.lesson.models import Lesson
from apps.django.main.lesson.sub.subserializers.lesson import LessonDetailSerializer
from apps.django.utils.serializers import WritableFromUserFieldMixin

__all__ = [
    "LessonField"
]


class LessonField(WritableFromUserFieldMixin):
    model = Lesson
    detail_serializer = LessonDetailSerializer
