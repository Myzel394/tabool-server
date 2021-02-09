from rest_framework import serializers

from ....models import Teacher

__all__ = [
    "ListStudentSerializer"
]


class ListStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "first_name", "last_name", "id"
        ]
