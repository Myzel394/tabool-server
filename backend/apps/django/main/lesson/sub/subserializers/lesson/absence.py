from rest_framework import serializers

from ....models import LessonAbsence

__all__ = [
    "LessonAbsenceSerializer"
]


class LessonAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonAbsence
        fields = [
            "reason", "is_signed", "id"
        ]
