from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.utils.serializers import IdMixinSerializer
from .room import RoomSerializer
from .subject import SubjectSerializer
from .teacher import TeacherSerializer
from ...models import LessonData

__all__ = [
    "LessonDataSerializer"
]


class LessonDataSerializer(IdMixinSerializer, WritableNestedModelSerializer):
    class Meta:
        model = LessonData
        fields = [
            "teacher", "room", "subject", "start_time", "end_time", "weekday", "id"
        ]
    
    teacher = TeacherSerializer()
    room = RoomSerializer()
    subject = SubjectSerializer()
    
    def create(self, validated_data):
        validated_data["associated_user"] = self.context["request"].user
        
        return super().create(validated_data)
