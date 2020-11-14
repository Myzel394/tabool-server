from typing import *

from django_common_utils.libraries.utils.text import create_short
from rest_framework import serializers

from apps.django.main.school_data.public.serializer_fields.room import RoomField
from apps.django.main.school_data.public.serializer_fields.subject import SubjectField
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField
from apps.django.utils.serializers import RandomIDSerializerMixin
from ...models import Modification

__all__ = [
    "ModificationListSerializer", "ModificationDetailSerializer"
]


class ModificationListSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Modification
        fields = [
            "start_datetime", "end_datetime", "modification_type", "truncated_information", "id"
        ]
    
    truncated_information = serializers.SerializerMethodField()
    
    def get_truncated_information(self, instance: Modification) -> Optional[str]:
        return create_short(instance.information) if instance.information else None


class ModificationDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Modification
        fields = [
            "new_room", "new_teacher", "new_subject", "start_datetime", "end_datetime", "information",
            "modification_type", "id"
        ]
    
    new_subject = SubjectField(required=False, detail=True)
    new_teacher = TeacherField(required=False, detail=True)
    new_room = RoomField(required=False, detail=True)
