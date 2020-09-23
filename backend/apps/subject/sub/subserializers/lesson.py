from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.utils.serializers import RandomIDSerializerMixin
from .lesson_data import LessonDataDetailSerializer, LessonDataListSerializer
from ...models import Lesson

__all__ = [
    "LessonListSerializer", "LessonDetailSerializer",
]


class LessonListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "id"
        ]
        read_only_fields = ["id"]
    
    lesson_data = LessonDataListSerializer()


class LessonDetailSerializer(RandomIDSerializerMixin, WritableNestedModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "lesson_data", "date", "attendance", "id"
        ]
        read_only_fields = ["id"]
    
    lesson_data = LessonDataDetailSerializer()
