from rest_framework import serializers

from apps.lesson.models import TeacherScoosoData
from apps.lesson.public.serializer_fields import TeacherField

__all__ = [
    "TeacherScoosoDataSerializer"
]


class TeacherScoosoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherScoosoData
        fields = [
            "code", "scooso_id", "teacher"
        ]
    
    teacher = TeacherField()

