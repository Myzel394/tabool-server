from .base import BaseUserSerializer

__all__ = [
    "ListUserSerializer"
]


class ListUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "first_name", "last_name", "id"
        ]
