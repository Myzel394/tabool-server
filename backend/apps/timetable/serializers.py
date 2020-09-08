from .models import Lesson, Room, Subject, Teacher, TimeTable

__all__ = [
    "SubjectSerializer", "TeacherSerializer", "RoomSerializer", "LessonSerializer", "TimeTableSerializer"
]

from ..utils.serializers import IdMixinSerializer


class SubjectSerializer(IdMixinSerializer):
    class Meta:
        model = Subject
        fields = ["name", "color", "id"]


class TeacherSerializer(IdMixinSerializer):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "id"]


class RoomSerializer(IdMixinSerializer):
    class Meta:
        model = Room
        fields = ["place", "id"]


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

class TimeTableSerializer(IdMixinSerializer):
    class Meta:
        model = TimeTable
        fields = ["lessons", "designation", "id"]
    
    lessons = LessonSerializer(many=True)
