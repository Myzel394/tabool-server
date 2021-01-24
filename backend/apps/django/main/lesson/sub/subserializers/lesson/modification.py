from rest_framework import serializers

from apps.django.main.event.models import Modification
from apps.django.main.school_data.public.serializer_fields.room import RoomField
from apps.django.main.school_data.public.serializer_fields.subject import SubjectField
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField

__all__ = [
    "LessonModificationSerializer"
]


class LessonModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modification
        fields = [
            "new_room", "new_teacher", "new_subject", "start_datetime", "end_datetime", "information",
            "modification_type", "id",
        ]
    
    new_subject = SubjectField(detail=True)
    new_teacher = TeacherField(detail=True)
    new_room = RoomField(detail=True)
