from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from apps.subject.sub.subserializers.lesson import LessonDetailSerializer
from apps.utils.serializers import RandomIDSerializerMixin
from ...models import Homework

__all__ = [
    "HomeworkListSerializer", "HomeworkDetailSerializer"
]


class HomeworkListSerializer(RandomIDSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = [
            "lesson", "due_date", "completed", "id"
        ]
    
    lesson = LessonDetailSerializer()


class HomeworkDetailSerializer(RandomIDSerializerMixin, WritableNestedModelSerializer):
    class Meta:
        model = Homework
        fields = [
            "lesson", "due_date", "information", "completed", "type", "id", "created_at", "edited_at",
        ]
    
    lesson = LessonDetailSerializer()
