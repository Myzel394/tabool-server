from apps.timetable.models import Lesson
from apps.utils.serializers import IdMixinSerializer
from apps.subject.sub.subserializers.room import RoomSerializer
from apps.subject.sub.subserializers.subject import SubjectSerializer
from apps.subject.sub.subserializers.teacher import TeacherSerializer
from ...models import Subject, Teacher, Room

__all__ = [
    "LessonSerializer"
]


class LessonSerializer(IdMixinSerializer):
    class Meta:
        model = Lesson
        fields = ["start_time", "end_time", "subject", "teacher", "room", "weekday", "id"]
    
    subject = SubjectSerializer()
    teacher = TeacherSerializer()
    room = RoomSerializer()
    
    @staticmethod
    def _create_subject(subject_data: dict) -> Subject:
        serializer = SubjectSerializer(data=subject_data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.save()
        
        return subject
    
    @staticmethod
    def _create_teacher(teacher_data: dict) -> Teacher:
        serializer = TeacherSerializer(data=teacher_data)
        serializer.is_valid(raise_exception=True)
        teacher = serializer.save()
        
        return teacher
    
    @staticmethod
    def _create_room(room_data: dict) -> Room:
        serializer = RoomSerializer(data=room_data)
        serializer.is_valid(raise_exception=True)
        room = serializer.save()
        
        return room
    
    def create(self, validated_data: dict) -> Lesson:
        subject_data = validated_data.pop("subject")
        teacher_data = validated_data.pop("teacher")
        room_data = validated_data.pop("room")
        
        subject = self._create_subject(subject_data)
        teacher = self._create_teacher(teacher_data)
        room = self._create_room(room_data)
        
        lesson = Lesson.objects.create(
            subject=subject,
            teacher=teacher,
            room=room,
            **validated_data
        )
        
        return lesson
