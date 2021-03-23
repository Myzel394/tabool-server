from rest_framework import serializers

from ....models import Teacher

__all__ = [
    "UserTeacherSerializer"
]


class UserTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "short_name"
        ]
