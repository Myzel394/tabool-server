from apps.django.main.school_data.public.serializer_fields.room import RoomField
from apps.django.main.school_data.public.serializer_fields.subject import SubjectField
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from ...models import Modification

__all__ = [
    "ModificationDetailSerializer"
]


class ModificationDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "modification"
    
    class Meta:
        model = Modification
        fields = [
            "new_room", "new_teacher", "new_subject", "start_datetime", "end_datetime", "information",
            "modification_type", "id"
        ]
    
    new_subject = SubjectField(required=False, detail=True)
    new_teacher = TeacherField(required=False, detail=True)
    new_room = RoomField(required=False, detail=True)
