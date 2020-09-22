from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.subject.sub.subserializers import LessonDetailSerializer, LessonListSerializer
from apps.utils.serializers import RandomIDSerializerMixin
from ...models import TeacherHomework

__all__ = [
    "TeacherHomeworkListSerializer", "TeacherHomeworkDetailSerializer"
]


class TeacherHomeworkListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = TeacherHomework
        fields = [
            "lesson", "due_date", "completed", "id"
        ]
    
    lesson = LessonListSerializer()


class TeacherHomeworkDetailSerializer(RandomIDSerializerMixin, WritableNestedModelSerializer):
    class Meta:
        model = TeacherHomework
        fields = [
            "lesson", "due_date", "information", "completed", "id"
        ]
    
    lesson = LessonDetailSerializer()
