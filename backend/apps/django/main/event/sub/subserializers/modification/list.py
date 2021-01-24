from typing import *

from django_common_utils.libraries.utils import create_short
from rest_framework import serializers

from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from .base import BaseModificationSerializer

if TYPE_CHECKING:
    from ....models import Modification

__all__ = [
    "ListModificationSerializer"
]


class ListModificationSerializer(BaseModificationSerializer):
    class Meta(BaseModificationSerializer.Meta):
        fields = [
            "lesson", "modification_type", "start_datetime", "end_datetime", "truncated_information", "id"
        ]
    
    lesson = LessonField()
    truncated_information = serializers.SerializerMethodField()
    
    @staticmethod
    def get_truncated_information(instance: "Modification") -> Optional[str]:
        if instance.instance:
            return create_short(instance.information)
        return
