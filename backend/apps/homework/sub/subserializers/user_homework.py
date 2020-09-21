from apps.subject.sub.subserializers import LessonSerializer
from apps.utils.serializers import IdMixinSerializer, NestedModelParentSerializerMixin, NestedModelSerializerField

from ...models import UserHomework

__all__ = [
    "UserHomeworkSerializer"
]


class UserHomeworkSerializer(IdMixinSerializer, NestedModelParentSerializerMixin):
    class Meta:
        model = UserHomework
        fields = [
            "lesson", "due_date", "information", "completed", "homework_type", "id", "created_at", "edited_at",
        ]
    
    lesson = NestedModelSerializerField(
        LessonSerializer
    )

# TODO: https://github.com/beda-software/drf-writable-nested
