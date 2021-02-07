from .base import BaseLessonSerializer

__all__ = [
    "DetailLessonSerializer"
]


class DetailLessonSerializer(BaseLessonSerializer):
    class Meta(BaseLessonSerializer.Meta):
        fields = [
            "course", "start_hour", "end_hour", "weekday", "id"
        ]
