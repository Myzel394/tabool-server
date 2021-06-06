from rest_framework import serializers

from .base import BaseTeacherSerializer

__all__ = [
    "DetailTeacherSerializer"
]


class DetailTeacherSerializer(BaseTeacherSerializer):
    class Meta(BaseTeacherSerializer.Meta):
        fields = [
            "first_name", "last_name", "short_name", "email", "gender", "id"
        ]

    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    email = serializers.ReadOnlyField(source="user.email")
    gender = serializers.ReadOnlyField(source="user.gender")
    id = serializers.ReadOnlyField(source="user.id")
