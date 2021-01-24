from .base import BaseEventSerializer

__all__ = [
    "ListEventSerializer"
]


class ListEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        fields = [
            "title", "start_datetime", "end_datetime", "id"
        ]
