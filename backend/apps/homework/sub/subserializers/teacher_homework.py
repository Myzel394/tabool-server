from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.subject.sub.subserializers import LessonDataSerializer, TeacherSerializer
from apps.utils.serializers import IdMixinSerializer

from ...models import TeacherHomework

__all__ = [
    "TeacherHomeworkSerializer"
]


class TeacherHomeworkSerializer(IdMixinSerializer, WritableNestedModelSerializer):
    class Meta:
        model = TeacherHomework
        fields = [
            "lesson", "due_date", "information", "completed", "homework_type", "id", "teacher"
        ]
    
    lesson = LessonDataSerializer()
    teacher = TeacherSerializer()
