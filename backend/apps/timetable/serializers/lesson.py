from apps.utils.serializers import IdMixinSerializer

from . import SubjectSerializer, TeacherSerializer, RoomSerializer
from ..models import Lesson, Subject, Teacher, Room

__all__ = [
    "LessonSerializer"
]


class LessonSerializer(IdMixinSerializer):
    class Meta:
        model = Lesson
        fields = ["start_time", "end_time", "subject", "teacher", "room", "id"]
    
    subject = SubjectSerializer()
    teacher = TeacherSerializer()
    room = RoomSerializer()
    
    def create(self, validated_data: dict) -> Lesson:
        subject_data = validated_data.pop("subject")
        teacher_data = validated_data.pop("teacher")
        room_data = validated_data.pop("room")
        
        subject = Subject.objects.create(**subject_data)
        teacher = Teacher.objects.create(**teacher_data)
        room = Room.objects.create(**room_data)
        
        lesson = Lesson.objects.create(
            subject=subject,
            teacher=teacher,
            room=room,
            **validated_data
        )
        
        return lesson