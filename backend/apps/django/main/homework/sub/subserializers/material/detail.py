from typing import *

from rest_framework import serializers

from apps.django.main.homework.models import Material
from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from .base import BaseMaterialSerializer
from ..mixins import SizeMixin

if TYPE_CHECKING:
    from ....models import Material

__all__ = [
    "DetailMaterialSerializer"
]


class DetailMaterialSerializer(BaseMaterialSerializer, SizeMixin):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "name", "added_at", "size", "id", "file", "is_deleted", "lesson"
        ]
    
    lesson = LessonField(detail=True)
    
    name = serializers.SerializerMethodField()
    
    def get_name(self, instance: Material):
        return instance.name or instance._original_filename
