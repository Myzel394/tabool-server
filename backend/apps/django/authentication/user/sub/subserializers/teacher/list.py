from rest_framework import serializers

from ....models import Teacher

__all__ = [
    "ListTeacherSerializer"
]


class ListTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "short_name", "last_name", "gender", "id"
        ]
    
    last_name = serializers.ReadOnlyField(source="user.last_name")
    gender = serializers.ReadOnlyField(source="user.gender")
    id = serializers.ReadOnlyField(source="user.id")
