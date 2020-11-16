from typing import *

from django_common_utils.libraries.utils.text import create_short
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.main.school_data.public.serializer_fields.room import RoomField
from apps.django.main.school_data.public.serializer_fields.subject import SubjectField
from apps.django.main.school_data.public.serializer_fields.teacher import TeacherField
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from ...models import Modification

__all__ = [
    "ModificationListSerializer", "ModificationDetailSerializer"
]


class ModificationListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "modification"
    
    class Meta:
        model = Modification
        fields = [
            "lesson", "modification_type", "truncated_information", "id"
        ]
    
    truncated_information = serializers.SerializerMethodField()
    lesson = LessonField(detail=True)
    
    def get_truncated_information(self, instance: Modification) -> Optional[str]:
        return create_short(instance.information) if instance.information else None


class ModificationDetailSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "modification"
    
    class Meta:
        model = Modification
        fields = [
            "new_room", "new_teacher", "new_subject", "lesson", "information", "modification_type", "id"
        ]
    
    lesson = LessonField()
    
    new_subject = SubjectField(required=False, detail=True)
    new_teacher = TeacherField(required=False, detail=True)
    new_room = RoomField(required=False, detail=True)
