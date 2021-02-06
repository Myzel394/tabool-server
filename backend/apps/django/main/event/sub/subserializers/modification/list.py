from .base import BaseModificationSerializer

__all__ = [
    "ListModificationSerializer",
]


class ListModificationSerializer(BaseModificationSerializer):
    class Meta(BaseModificationSerializer.Meta):
        fields = [
            "lesson", "lesson_date",
            "modification_type"
        ]
    
    lesson = DetailLessonSerializer()
