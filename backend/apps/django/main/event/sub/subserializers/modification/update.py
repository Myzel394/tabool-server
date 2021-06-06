from apps.django.authentication.user.public.serializer_fields.teacher import TeacherField
from apps.django.main.course.public.serializer_fields.room import RoomField
from apps.django.main.course.public.serializer_fields.subject import SubjectField
from .base import BaseModificationSerializer

__all__ = [
    "UpdateModificationSerializer"
]


class UpdateModificationSerializer(BaseModificationSerializer):
    class Meta(BaseModificationSerializer.Meta):
        fields = [
            "new_room", "new_subject", "new_teacher", "information", "modification_type",
        ]

    new_room = RoomField()
    new_subject = SubjectField()
    new_teacher = TeacherField()
