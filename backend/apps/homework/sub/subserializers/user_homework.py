from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.subject.sub.subserializers.lesson import LessonDetailSerializer
from apps.utils.serializers import IdMixinSerializer
from ...models import UserHomework

__all__ = [
    "UserHomeworkListSerializer", "UserHomeworkDetailSerializer"
]


class UserHomeworkListSerializer(IdMixinSerializer):
    class Meta:
        model = UserHomework
        fields = [
            "lesson", "due_date", "completed", "id"
        ]
    
    lesson = LessonDetailSerializer()


class UserHomeworkDetailSerializer(IdMixinSerializer, WritableNestedModelSerializer):
    class Meta:
        model = UserHomework
        fields = [
            "lesson", "due_date", "information", "completed", "homework_type", "id", "created_at", "edited_at",
        ]
    
    lesson = LessonDetailSerializer()
