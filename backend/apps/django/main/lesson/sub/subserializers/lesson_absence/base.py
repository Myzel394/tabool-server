from rest_framework import serializers

from ....models import LessonAbsence

__all__ = [
    "BaseLessonAbsenceSerializer"
]


class BaseLessonAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonAbsence
        fields = [
            "reason", "is_signed"
        ]
