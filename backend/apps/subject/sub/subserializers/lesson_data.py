from drf_writable_nested.serializers import WritableNestedModelSerializer

from apps.utils.serializers import IdMixinSerializer
from .room import RoomDetailSerializer
from .subject import SubjectDetailSerializer
from .teacher import TeacherDetailSerializer
from ...models import LessonData

__all__ = [
    "LessonDataListSerializer", "LessonDataDetailSerializer"
]


class LessonDataListSerializer(IdMixinSerializer):
    class Meta:
        model = LessonData
        fields = [
            "subject", "start_time", "end_time", "weekday", "id"
        ]
    
    subject = SubjectDetailSerializer()


class LessonDataDetailSerializer(IdMixinSerializer, WritableNestedModelSerializer):
    class Meta:
        model = LessonData
        fields = [
            "teacher", "room", "subject", "start_time", "end_time", "weekday", "id"
        ]
    
    teacher = TeacherDetailSerializer()
    room = RoomDetailSerializer()
    subject = SubjectDetailSerializer()
    
    def create(self, validated_data):
        validated_data["associated_user"] = self.context["request"].user
        
        return super().create(validated_data)
