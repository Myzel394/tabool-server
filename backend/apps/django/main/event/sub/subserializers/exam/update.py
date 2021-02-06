from .base import BaseExamSerializer

__all__ = [
    "UpdateExamSerializer"
]


class UpdateExamSerializer(BaseExamSerializer):
    class Meta(BaseExamSerializer.Meta):
        fields = [
            "date", "title", "information"
        ]
