from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from .base import BaseMaterialSerializer
from ..mixins import SizeMixin

__all__ = [
    "DetailMaterialSerializer"
]


class DetailMaterialSerializer(BaseMaterialSerializer, SizeMixin):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "name", "added_at", "size", "id", "file", "is_deleted", "lesson"
        ]
    
    lesson = LessonField(detail=True)
