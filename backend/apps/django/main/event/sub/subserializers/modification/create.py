from apps.django.authentication.user.public.serializer_fields.teacher import TeacherField
from apps.django.main.course.public.serializer_fields.room import RoomField
from apps.django.main.course.public.serializer_fields.subject import SubjectField
from apps.django.main.timetable.public.serializer_fields.lesson import LessonField
from .base import BaseModificationSerializer

__all__ = [
    "CreateModificationSerializer"
]


class CreateModificationSerializer(BaseModificationSerializer):
    class Meta(BaseModificationSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "new_room", "new_subject", "new_teacher", "information", "modification_type",
        ]
    
    lesson = LessonField()
    new_room = RoomField(required=False, allow_null=True)
    new_subject = SubjectField(required=False, allow_null=True)
    new_teacher = TeacherField(required=False, allow_null=True)
