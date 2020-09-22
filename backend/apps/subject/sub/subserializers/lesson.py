from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.utils.serializers import IdMixinSerializer
from .lesson_data import LessonDataDetailSerializer, LessonDataListSerializer
from ...models import Lesson

__all__ = [
    "LessonListSerializer", "LessonDetailSerializer",
]


class LessonListSerializer(IdMixinSerializer):
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "attendance", "id"
        ]
    
    lesson_data = LessonDataListSerializer()


class LessonDetailSerializer(IdMixinSerializer, WritableNestedModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "attendance", "id"
        ]
    
    lesson_data = LessonDataDetailSerializer()
