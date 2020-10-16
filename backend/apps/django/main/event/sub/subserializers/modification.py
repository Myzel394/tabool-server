from apps.django.main.school_data.public.serializer_fields import RoomField, SubjectField, TeacherField
from apps.django.utils.serializers import RandomIDSerializerMixin
from ...models import Modification

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
