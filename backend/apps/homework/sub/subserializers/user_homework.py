from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.subject.sub.subserializers import LessonDataSerializer
from apps.utils.serializers import IdMixinSerializer

from ...models import UserHomework

__all__ = [
    "UserHomeworkSerializer"
]


class UserHomeworkSerializer(IdMixinSerializer, WritableNestedModelSerializer):
    class Meta:
        model = UserHomework
        fields = [
            "lesson", "due_date", "information", "completed", "homework_type", "id", "created_at", "edited_at",
        ]
    
    lesson = LessonDataSerializer()
