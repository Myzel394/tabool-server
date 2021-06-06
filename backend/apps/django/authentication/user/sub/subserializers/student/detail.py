from rest_framework import serializers

from .base import BaseStudentSerializer
from ..teacher import DetailTeacherSerializer

__all__ = [
    "DetailStudentSerializer"
]


class DetailStudentSerializer(BaseStudentSerializer):
    class Meta(BaseStudentSerializer.Meta):
        fields = [
            "main_teacher", "class_number", "first_name", "last_name", "email", "gender", "id"
        ]

    main_teacher = DetailTeacherSerializer()

    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    email = serializers.ReadOnlyField(source="user.email")
    gender = serializers.ReadOnlyField(source="user.gender")
    id = serializers.ReadOnlyField(source="user.id")
