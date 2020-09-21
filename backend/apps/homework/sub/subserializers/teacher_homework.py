from apps.subject.sub.subserializers import LessonSerializer, TeacherSerializer
from apps.utils.serializers import IdMixinSerializer, NestedModelSerializerField

from ...models import TeacherHomework

__all__ = [
    "TeacherHomeworkSerializer"
]


class TeacherHomeworkSerializer(IdMixinSerializer):
    class Meta:
        model = TeacherHomework
        fields = [
            "lesson", "due_date", "information", "completed", "homework_type", "id", "teacher"
        ]
    
    lesson = NestedModelSerializerField(
        LessonSerializer
    )
    
    teacher = NestedModelSerializerField(
        TeacherSerializer
    )
