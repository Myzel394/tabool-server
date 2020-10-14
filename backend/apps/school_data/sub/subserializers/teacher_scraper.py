from rest_framework import serializers

from ...models import Teacher

__all__ = [
    "TeacherScraperSerializer"
]


class TeacherScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "first_name", "last_name", "short_name", "email"
        ]
