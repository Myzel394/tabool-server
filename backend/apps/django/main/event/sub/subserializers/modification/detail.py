from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.main.school_data.public.serializer_fields.room import RoomField
from apps.django.main.school_data.public.serializer_fields.subject import SubjectField
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField
from .base import BaseModificationSerializer

__all__ = [
    "DetailModificationSerializer"
]


class DetailModificationSerializer(BaseModificationSerializer):
    class Meta(BaseModificationSerializer.Meta):
        fields = [
            "new_room", "new_teacher", "new_subject", "start_datetime", "end_datetime", "information",
            "modification_type", "id", "lesson"
        ]
    
    new_subject = SubjectField(detail=True)
    new_teacher = TeacherField(detail=True)
    new_room = RoomField(detail=True)
    lesson = LessonField(detail=True)
