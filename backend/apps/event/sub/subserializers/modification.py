from apps.lesson.models import Modification
from apps.lesson.public.serializer_fields import RoomField, SubjectField, TeacherField
from apps.utils.serializers import RandomIDSerializerMixin

__all__ = [
    "ModificationListSerializer", "ModificationDetailSerializer"
]


class ModificationListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Modification
        fields = [
            "start_datetime", "end_datetime", "new_subject", "new_teacher", "new_room", "id"
        ]
    
    new_subject = SubjectField()
    new_teacher = TeacherField()
    new_room = RoomField()


class ModificationDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Modification
        fields = [
            "new_room", "new_teacher", "new_subject", "start_datetime", "end_datetime", "information",
            "modification_type", "id"
        ]
    
    new_subject = SubjectField()
    new_teacher = TeacherField()
    new_room = RoomField()