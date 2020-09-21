from apps.utils.serializers import IdMixinSerializer, NestedModelParentSerializerMixin, NestedModelSerializerField
from .room import RoomSerializer
from .subject import SubjectSerializer
from .teacher import TeacherSerializer
from ...models import Lesson

__all__ = [
    "LessonSerializer"
]


class LessonSerializer(IdMixinSerializer, NestedModelParentSerializerMixin):
    class Meta:
        model = Lesson
        fields = [
            "teacher", "room", "subject", "start_time", "end_time", "weekday", "id"
        ]
    
    teacher = NestedModelSerializerField(TeacherSerializer)
    room = NestedModelSerializerField(RoomSerializer)
    subject = NestedModelSerializerField(SubjectSerializer)
    
    def create(self, validated_data):
        validated_data["associated_user"] = self.context["request"].user
        
        return super().create(validated_data)
