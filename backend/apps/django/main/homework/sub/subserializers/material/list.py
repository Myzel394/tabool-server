from apps.django.main.lesson.public.serializer_fields.lesson import LessonField
from .base import BaseMaterialSerializer

__all__ = [
    "ListMaterialSerializer"
]


class ListMaterialSerializer(BaseMaterialSerializer):
    class Meta(BaseMaterialSerializer.Meta):
        fields = [
            "lesson", "name", "added_at", "id"
        ]
    
    lesson = LessonField()
