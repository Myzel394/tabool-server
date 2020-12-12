from typing import *

from django_common_utils.libraries.utils.text import create_short
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from apps.django.utils.serializers import PreferredIdsMixin, RandomIDSerializerMixin
from .modification import ModificationDetailSerializer
from ...models import Modification

__all__ = [
    "ModificationListSerializer", "ModificationDetailSerializer"
]


class ModificationListSerializer(RandomIDSerializerMixin, PreferredIdsMixin):
    preferred_id_key = "modification"
    
    class Meta:
        model = Modification
        fields = [
            "lesson", "modification_type", "start_datetime", "end_datetime", "truncated_information", "id"
        ]
    
    truncated_information = serializers.SerializerMethodField()
    lesson = LessonField()
    
    def get_truncated_information(self, instance: Modification) -> Optional[str]:
        return create_short(instance.information) if instance.information else None


class ModificationDetailEndpointSerializer(ModificationDetailSerializer):
    class Meta(ModificationDetailSerializer.Meta):
        fields = ModificationDetailSerializer.Meta.fields + [
            "lesson"
        ]
    
    lesson = LessonField(detail=True)
