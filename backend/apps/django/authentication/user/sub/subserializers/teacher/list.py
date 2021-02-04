from rest_framework import serializers

from ....models import Teacher

__all__ = [
    "ListTeacherSerializer"
]


class ListTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["short_name", "last_name", "id", "gender"]
