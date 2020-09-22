from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.subject.sub.subserializers import LessonDetailSerializer, LessonListSerializer
from apps.utils.serializers import IdMixinSerializer
from ...models import TeacherHomework

__all__ = [
    "TeacherHomeworkListSerializer", "TeacherHomeworkDetailSerializer"
]


class TeacherHomeworkListSerializer(IdMixinSerializer):
    class Meta:
        model = TeacherHomework
        fields = [
            "lesson", "due_date", "completed", "id"
        ]
    
    lesson = LessonListSerializer()


class TeacherHomeworkDetailSerializer(IdMixinSerializer, WritableNestedModelSerializer):
    class Meta:
        model = TeacherHomework
        fields = [
            "lesson", "due_date", "information", "completed", "id"
        ]
    
    lesson = LessonDetailSerializer()
